import cv2
import numpy as np
from image_processing import methods


class ImageProcessing:
    """
    Class with image processing operations
    """
    def __init__(self, image_url, params):
        """

        @param image_url: url to image to process
        @param params: parameters for image processing
        """
        self.image = cv2.imread(image_url)
        self.params = params

    def gaussian(self):
        """
        @return image with added gaussian noise
        """
        return methods.gaussian(self.image, self.params["intensity"])

    def sp(self):
        """
        @return image with added salt & pepper
        """
        return methods.sp(self.image, self.params["intensity"])

    def rain(self):
        """
        @return image with added rain
        """
        return methods.rain(self.image, int(self.params["kernel_size"]), int(self.params["angle"]),
                            float(self.params["intensity"]))

    def color_balance(self):
        """
        @return image with changed color balance
        """
        image = np.array(self.image).astype(int)
        result = methods.color_balance(image, self.params["blue"], self.params["green"], self.params["red"])
        if self.params["saturation"] != 1:
            result = methods.color_balance(result, self.params["saturation"], self.params["saturation"],
                                           self.params["saturation"])
        return result

    def remove_rain(self):
        """
        @return image with removed rain
        """
        print(self.params)
        return methods.remove_rain(self.image, int(self.params["radius"]), float(self.params["epsilon"]))

    def contrast_and_brightness(self):
        """
        @return image with changed brightness and contrast
        """
        return methods.contrast_and_brightness(self.image, alpha=self.params["contrast"],
                                               beta=self.params["brightness"])
