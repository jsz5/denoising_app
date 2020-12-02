import os

import cv2
import numpy as np
from django.utils.crypto import get_random_string
from django.conf import settings


def get_full_url(url):
    return f"{settings.BASE_DIR}{url}"


def image_to_numpy(image):
    image = np.asarray(bytearray(image.read()), dtype="uint8")
    return cv2.imdecode(image, cv2.IMREAD_COLOR)


def save_image(image):
    name = f"{get_random_string()}.png"
    cv2.imwrite(f"{settings.MEDIA_ROOT}/{name}", image)
    return f"{settings.MEDIA_URL}{name}"


def remove_image(url):
    if os.path.exists(url):
        os.remove(url)
