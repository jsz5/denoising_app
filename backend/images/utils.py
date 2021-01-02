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


def save_image(image, pil=False):
    name = f"{get_random_string()}.png"
    url = f"{settings.MEDIA_ROOT}/{name}"
    if pil:
        image.save(url)
    else:
        cv2.imwrite(url, image)
    return f"{settings.MEDIA_URL}{name}"


def remove_image(url):
    if os.path.exists(url):
        os.remove(url)
