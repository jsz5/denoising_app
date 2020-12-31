import cv2
import numpy as np
from image_processing import methods


class ImageProcessing:
    def __init__(self, image_url, params):
        self.image = cv2.imread(image_url)
        self.params = params

    def gaussian(self, mean=0):
        return methods.gaussian(self.image, self.params["intensity"])

    def sp(self):
        return methods.sp(self.image, self.params["intensity"])

    def rain(self):
        return methods.rain(self.image, self.params["kernel_size"], self.params["angle"],
                            self.params["intensity"])

    def contrast_and_brightness(self):
        return methods.contrast_and_brightness(self.image, alpha=self.params["contrast"],
                                               beta=self.params["brightness"])
