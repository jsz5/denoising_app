import os

import cv2
import numpy as np
from django.utils.crypto import get_random_string
from django.conf import settings


def get_full_url(url):
    """
    @return full url to file
    """
    return f"{settings.BASE_DIR}{url}"


def image_to_numpy(image):
    """
    @param image: input image
    @return image converted to numpy
    """
    image = np.asarray(bytearray(image.read()), dtype="uint8")
    return cv2.imdecode(image, cv2.IMREAD_COLOR)


def save_image(image):
    """
    @param image: (numpy array or PIL) input image
    @return url to saved image in file storage
    """
    name = f"{get_random_string()}.png"
    url = f"{settings.MEDIA_ROOT}/{name}"
    if type(image) == np.ndarray:
        cv2.imwrite(url, image)
    else:
        image.save(url)

    return f"{settings.MEDIA_URL}{name}"


def remove_image(url):
    """
    Deletes image from file storage
    @param url: image url
    """
    if os.path.exists(url):
        os.remove(url)
