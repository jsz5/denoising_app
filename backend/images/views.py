import logging

from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from images.config import WEBAPP_LOGS
from images.image_processing import ImageProcessing
from images.serializers import NoiseTypeSerializer, ImageProcessingSerializer, ImageSerializer
from images.utils import image_to_numpy, save_image, remove_image, get_full_url
from neural_network.testing.denoising import Denoising

logging.basicConfig(filename=WEBAPP_LOGS, level=logging.DEBUG)
class ImageProcessingView(APIView):
    """
    Processes input image and optionally deletes 'old_image'. Processed image is saved as a new image in file storage.
    """

    def post(self, request, *args, **kwargs):
        """
        @return url to processed image
        """
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
    """
    Removes noise from input image and removes image with noise. Processed image is saved as a new image in file storage.
    """

    def post(self, request, *args, **kwargs):
        """
        @return url to image with removed noise
        """
        serializer = NoiseTypeSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        try:
            predicted = Denoising(image=serializer.data["image_url"], noise=serializer.data["noise"]).denoise()
            remove_image(serializer.data["image_url"])
            return Response(save_image(predicted))
        except RuntimeError as e:
            logging.error(f"Remove noise view: {e}")
            return HttpResponse("Wystąpił błąd. Za mało pamięci.", status=422)

    def get_serializer_context(self):
        return {"request": self.request.data}


class UploadImage(APIView):
    """
    Uploads image to file storage and returns url to it.
    """
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        """
        @return url to uploaded image
        """
        image = image_to_numpy(request.data["new_image"])
        return Response(save_image(image))


class RemoveImage(APIView):
    """
    Removes image from file storage
    """
    def post(self, request, *args, **kwargs):
        try:
            serializer = ImageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            remove_image(get_full_url(serializer.data["image_url"]))
        except FileNotFoundError as e:
            logging.error(f"Remove image view: {e}")
            return HttpResponse("Obraz nie istnieje.", status=404)
        return Response("Usunięto pomyślnie.")
