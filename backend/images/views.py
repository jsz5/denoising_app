from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.http import FileResponse
from images.image_processing import Noise
from images.neural_network.denoising import Denoising
from images.serializers import NoiseTypeSerializer, AddNoiseSerializer


class AddNoiseView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = AddNoiseSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        noise = Noise(image=serializer.data["file"], noise_params=serializer.data["noise_params"])
        result = getattr(noise, serializer.data["noise"])()
        return FileResponse(result, content_type="image/png")

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
