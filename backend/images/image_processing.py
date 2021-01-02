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
        return methods.rain(self.image, int(self.params["kernel_size"]), int(self.params["angle"]),
                            float(self.params["intensity"]))

    def color_balance(self):
        image = np.array(self.image).astype(int)
        result = methods.color_balance(image, self.params["blue"], self.params["green"], self.params["red"])
        if self.params["saturation"] != 1:
            result = methods.color_balance(result, self.params["saturation"], self.params["saturation"],
                                           self.params["saturation"])
        return result

    def remove_rain(self):
        print(self.params)
        return methods.remove_rain(self.image, int(self.params["radius"]), float(self.params["epsilon"]))

    def contrast_and_brightness(self):
        return methods.contrast_and_brightness(self.image, alpha=self.params["contrast"],
                                               beta=self.params["brightness"])
