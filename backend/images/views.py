import urllib

from django.conf import settings
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from images.image_processing import ImageProcessing
from images.serializers import NoiseTypeSerializer, ImageProcessingSerializer, ImageSerializer
from images.utils import image_to_numpy, save_image, remove_image, get_full_url
from neural_network.denoising import Denoising


class ImageProcessingView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageProcessingSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        image_processing = ImageProcessing(image_url=serializer.data["image_url"], params=serializer.data["params"])
        result = getattr(image_processing, serializer.data["method"])()
        if "old_image" in serializer.data and serializer.data['old_image']:
            remove_image(serializer.data['old_image'])
        return Response(save_image(result))

    def get_serializer_context(self):
        return {"request": self.request.data}


class RemoveNoise(APIView):
    def post(self, request, *args, **kwargs):
        serializer = NoiseTypeSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        try:
            predicted = Denoising(image=serializer.data["image_url"], noise=serializer.data["noise"]).denoise()
            remove_image(serializer.data["image_url"])
            return Response(save_image(predicted, pil=True))
        except RuntimeError:
            return HttpResponse("Wystąpił błąd. Za mało pamięci.", status=422)

    def get_serializer_context(self):
        return {"request": self.request.data}


class UploadImage(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        image = image_to_numpy(request.data["new_image"])
        return Response(save_image(image))


class SaveImageDataURL(APIView):
    def post(self, request, *args, **kwargs):
        try:
            image = urllib.request.urlopen(request.data["file"])
            name = f"{get_random_string()}.png"
            with open(f"{settings.MEDIA_ROOT}/{name}", 'wb') as f:
                f.write(image.file.read())
            if "old_url" in request.data:
                remove_image(get_full_url(request.data['old_url']))
        except FileNotFoundError:
            return HttpResponse("Obraz nie istnieje.", status=404)
        return Response(f"{settings.MEDIA_URL}{name}")


class RemoveImage(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = ImageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            remove_image(get_full_url(serializer.data["image_url"]))
        except FileNotFoundError:
            return HttpResponse("Obraz nie istnieje.", status=404)
        return Response("Usunięto pomyślnie.")
