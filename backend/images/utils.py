import cv2
import numpy as np
from django.utils.crypto import get_random_string
from django.conf import settings


def image_to_numpy(image):
    image = np.asarray(bytearray(image.read()), dtype="uint8")
    return cv2.imdecode(image, cv2.IMREAD_COLOR)


def image_to_media(image):
    name = f"{get_random_string()}.png"
    cv2.imwrite(f"{settings.MEDIA_ROOT}/{name}", image)
    return f"{settings.MEDIA_URL}{name}"
