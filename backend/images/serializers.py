import json

from rest_framework import serializers

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


class ImageProcessingSerializer(serializers.Serializer):
    params = serializers.SerializerMethodField()
    old_image = serializers.CharField(required=False)
    method = serializers.CharField()
    image_url = serializers.CharField()

    default_error_messages = {
        "invalid_data": "Błędne dane",
        "img_doesnt_exists": "Obraz o podanym url nie istnieje",
    }

    def get_params(self, obj):
        print(obj)
        if "params" not in self.context["request"].keys():
            self.fail("invalid_data")
        params = self.context["request"]["params"]
        if obj["method"] in ["gaussian", "sp"] and "intensity" not in params:
            self.fail("invalid_data")
        if obj["method"] == "rain" and any(param not in params for param in ["intensity", "kernel_size", "angle"]):
            self.fail("invalid_data")
        if obj["method"] == "color_balance" and any(
                param not in params for param in ["red", "green", "blue", "saturation"]):
            self.fail("invalid_data")
        if obj["method"] == "contrast_and_brightness" and any(
                param not in params for param in ["contrast", "brightness"]):
            self.fail("invalid_data")
        if obj["method"] == "remove_rain" and any(
                param not in params for param in ["radius", "epsilon"]):
            self.fail("invalid_data")
        return json.loads(params)

    def validate_method(self, value):
        if value not in ["gaussian", "sp", "rain","contrast_and_brightness","color_balance", "remove_rain"]:
            self.fail("invalid_data")
        return value

    def validate(self, attrs):
        try:
            attrs["image_url"] = get_full_url(attrs["image_url"])
            if "old_image" in attrs:
                attrs["old_image"] = get_full_url(attrs["old_image"])
        except FileNotFoundError:
            self.fail("img_doesnt_exists")
        return attrs


class ImageSerializer(serializers.Serializer):
    image_url = serializers.CharField()


class ContrastBrightnessSerializer(ImageSerializer):
    contrast = serializers.FloatField()
    brightness = serializers.FloatField()
