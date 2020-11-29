from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from images.image_processing import Noise
from images.serializers import NoiseTypeSerializer


class AddNoiseView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = NoiseTypeSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        noise = Noise(image=serializer.data["file"], noise_params=serializer.data["noise_params"])
        result = getattr(noise, serializer.data["noise"])()
        return HttpResponse(result, content_type="image")

    def get_serializer_context(self):
        return {"file": self.request.FILES["file"], "request": self.request.data}


class RemoveNoise(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = NoiseTypeSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        noise = Noise(image=serializer.data["file"], noise_params=serializer.data["noise_params"])
        result = getattr(noise, serializer.data["noise"])()
        return HttpResponse(result, content_type="image")