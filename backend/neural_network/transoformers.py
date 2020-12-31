import cv2
import numpy as np


class ToTensor(object):
    """Convert ndarrays image to Tensor."""

    def __call__(self, image):
        return self.normalize(image)

    def normalize(self, image):
        # swap color axis because
        # numpy image: H x W x C
        # torch image: C X H X W
        image = image.transpose((2, 0, 1))
        image = image.astype(np.float32) / 255.
        return image


class GuidedFilterTransform(object):
    def __call__(self, rain_image):
        low_frequency = np.empty(rain_image.shape)
        new_high_frequency = np.empty(rain_image.shape)
        result = np.empty(rain_image.shape)
        r = 8
        epsilon = 0.1 ** 2
        epsilon *= 255 ** 2
        guided_filter = cv2.ximgproc.createGuidedFilter(rain_image, r, epsilon)
        low_frequency = guided_filter.filter(rain_image, low_frequency)
        high_frequency = cv2.subtract(rain_image, low_frequency)
        kernel_sharpening = np.array([[-1, -1, -1],
                                      [-1, 9, -1],
                                      [-1, -1, -1]])
        low_edges = cv2.filter2D(low_frequency, -1, kernel_sharpening)

        guided_filter2 = cv2.ximgproc.createGuidedFilter(high_frequency, r, epsilon)
        new_high_frequency = guided_filter2.filter(low_edges, new_high_frequency)
        recovered = cv2.addWeighted(new_high_frequency, 0.5, low_edges, 0.5, 0)
        cleared = np.minimum(recovered, rain_image)
        b = 0.8
        refined = (b * cleared) + ((1 - b) * recovered)
        refined = np.uint8(refined)
        guided_filter3 = cv2.ximgproc.createGuidedFilter(cleared, r, epsilon)
        result = guided_filter3.filter(refined, result)

        return result
