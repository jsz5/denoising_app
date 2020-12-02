import os
import base64
import io
import urllib

from PIL import Image

import cv2
from django.conf import settings
from django.http import FileResponse
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from images.image_processing import Noise
from images.neural_network.denoising import Denoising
from images.serializers import NoiseTypeSerializer, AddNoiseSerializer
from images.utils import image_to_numpy, save_image, remove_image, get_full_url


class AddNoiseView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = AddNoiseSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        print(cv2.imread('/code/media/1xlimYtFGsBl.png'))
        print(serializer.data['image_url'])
        noise = Noise(image_url=serializer.data["image_url"], noise_params=serializer.data["noise_params"])
        result = getattr(noise, serializer.data["noise"])()
        print(serializer.data['old_image'])
        if serializer.data['old_image']:
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

            return FileResponse(predicted, content_type="image/png")
        except RuntimeError:
            return HttpResponse("Wystąpił błąd. Za mało pamięci.")

    def get_serializer_context(self):
        return {"request": self.request.data}


class UploadImage(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        image = image_to_numpy(request.data["new_image"])
        return Response(save_image(image))


class SaveImageDataURL(APIView):
    def post(self, request, *args, **kwargs):
        image = urllib.request.urlopen(request.data["file"])
        name = f"{get_random_string()}.png"
        with open(f"{settings.MEDIA_ROOT}/{name}", 'wb') as f:
            f.write(image.file.read())
        if "old_url" in request.data:
            remove_image(get_full_url(request.data['old_url']))

        return Response(f"{settings.MEDIA_URL}{name}")


class RemoveImage(APIView):
    def post(self, request, *args, **kwargs):
        remove_image(get_full_url(request.data['image_url']))
        return Response("Usunięto pomyślnie")
