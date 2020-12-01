import os

from django.conf import settings
from django.http import FileResponse
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from images.image_processing import Noise
from images.neural_network.denoising import Denoising
from images.serializers import NoiseTypeSerializer, AddNoiseSerializer
from images.utils import image_to_numpy, image_to_media


class AddNoiseView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = AddNoiseSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        noise = Noise(image=serializer.data["file"], noise_params=serializer.data["noise_params"])
        result = getattr(noise, serializer.data["noise"])()
        old_url = f"{settings.BASE_DIR}{serializer.data['url']}"
        print(os.path.exists(old_url))
        print(old_url)
        if os.path.exists(old_url):
            os.remove(old_url)
        return Response(image_to_media(result))

    def get_serializer_context(self):
        return {"file": self.request.FILES["file"], "request": self.request.data}


class RemoveNoise(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = NoiseTypeSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        try:
            predicted = Denoising(image=serializer.data["file"], noise=serializer.data["noise"]).denoise()

            return FileResponse(predicted, content_type="image/png")
        except RuntimeError:
            return HttpResponse("Wystąpił błąd. Za mało pamięci.")

    def get_serializer_context(self):
        return {"file": self.request.FILES["file"], "request": self.request.data}


class UploadImage(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        image = image_to_numpy(request.data["file"])
        return Response(image_to_media(image))
