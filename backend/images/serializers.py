import json

from rest_framework import serializers
import numpy as np
import cv2


class NoiseTypeSerializer(serializers.Serializer):
    noise = serializers.CharField()
    file = serializers.SerializerMethodField()

    default_error_messages = {
        "invalid_noise": "Błędny typ zakłócenia",
        "invalid_format": "Błędny format"
    }

    def validate_noise(self, value):
        if value not in ["gaussian", "sp", "rain"]:
            self.fail("invalid_noise")
        return value

    def validate_file(self, value):
        if not value.name.endswith((".png", ".jpg", ".jpeg")):
            self.fail("invalid_format")
        return value

    def get_file(self, obj):
        file = self.context["file"]
        self.validate_file(file)
        image = np.asarray(bytearray(file.read()), dtype="uint8")
        return cv2.imdecode(image, cv2.IMREAD_COLOR)


class AddNoiseSerializer(NoiseTypeSerializer):
    noise_params = serializers.SerializerMethodField()

    default_error_messages = {
        "invalid_data": "Błędne dane",
    }

    def get_noise_params(self, obj):
        if "noise_params" not in self.context["request"].keys():
            self.fail("invalid_data")
        noise_params = self.context["request"]["noise_params"]
        if obj["noise"] == "gaussian" and "sigma" not in noise_params:
            self.fail("invalid_data")
        if obj["noise"] == "sp" and "probability" not in noise_params:
            self.fail("invalid_data")
        if obj["noise"] == "rain" and any(param not in noise_params for param in ["intensity", "kernel_size", "angle"]):
            self.fail("invalid_data")
        return json.loads(noise_params)
