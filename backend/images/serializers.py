import json

from rest_framework import serializers

from django.conf import settings

from images.utils import get_full_url


class NoiseTypeSerializer(serializers.Serializer):
    noise = serializers.CharField()
    image_url = serializers.CharField()

    default_error_messages = {
        "invalid_noise": "Błędny typ zakłócenia"
    }

    def validate_noise(self, value):
        if value not in ["gaussian", "sp", "rain"]:
            self.fail("invalid_noise")
        return value

    def validate(self, attrs):
        attrs["image_url"] = get_full_url(attrs["image_url"])
        return attrs




class AddNoiseSerializer(NoiseTypeSerializer):
    noise_params = serializers.SerializerMethodField()
    old_image = serializers.CharField()

    default_error_messages = {
        "invalid_data": "Błędne dane",
    }

    def get_noise_params(self, obj):
        if "noise_params" not in self.context["request"].keys():
            self.fail("invalid_data")
        noise_params = self.context["request"]["noise_params"]
        if obj["noise"] in ["gaussian", "sp"] and "intensity" not in noise_params:
            self.fail("invalid_data")
        if obj["noise"] == "rain" and any(param not in noise_params for param in ["intensity", "kernel_size", "angle"]):
            self.fail("invalid_data")
        return json.loads(noise_params)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["old_image"] = get_full_url(attrs["old_image"])
        return attrs
