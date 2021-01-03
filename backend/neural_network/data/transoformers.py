import cv2
import numpy as np

from image_processing.methods import remove_rain


class ToTensor(object):
    """Convert ndarray  to Tensor."""

    def __call__(self, sample):
        """

        @param sample (tuple|ndarray): numpy image|images
        @return tensor image
        """
        if type(sample) == tuple:
            image, noise_image = sample
            return self.normalize(image), self.normalize(noise_image)
        else:
            return self.normalize(sample)

    def normalize(self, image):
        """
        @param image (numpy): image axis are  H x W x C
        @return tensor of normalized image in range [0,1] with axis C X H X W
        """
        image = image.transpose((2, 0, 1))
        image = image.astype(np.float32) / 255.
        return image


class MedianFilterTransform(object):
    """
    Apply median filter with kernel_size=5 to image sample
    """

    def __call__(self, sample):
        """
        @param sample: sample of images: original image and image with noise
        @return (tuple) original image and noise image with median filter
        """
        image, noise_image = sample
        median = cv2.medianBlur(noise_image, 5)
        return image, median


class GuidedFilterTransform(object):
    """
    Remove rain from image with algorithm that uses guided filter

    """

    def __call__(self, sample):
        """
        @param sample: sample of images: original image and image with rain
        @return (tuple) original image and image with removed rain
        """
        image, rain_image = sample
        result = remove_rain(rain_image, r=8, epsilon=0.1)
        return image, result
