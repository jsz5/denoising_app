import copy
import logging
import os
import random
from math import sqrt
import cv2
from neural_network.config import DATA_LOGS_FILE
from shutil import copy as shutil_copy
from image_processing import methods

logging.basicConfig(filename=DATA_LOGS_FILE, level=logging.DEBUG)


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


class Noise:
    def __init__(self, image_path, output_path, image_name):
        """
        @param image_path:  path to folder with original images
        @param output_path: path to folder with images with added noise
        @param image_name: original image name
        """
        self.image = cv2.imread(f"{image_path}/{image_name}")
        self.original = copy.deepcopy(self.image)
        self.image_name = image_name
        self.output_path = output_path
        create_directory(output_path)

    def resize(self, path, image_size, crop=True):
        """
        Changes size of original image and saves it to folder.
        @param path: path to folder where resized image will be saved
        @param image_size: new image size
        @param crop: determines if image will be cropped to be a square (default True)
        """
        height, width, _ = self.image.shape
        if height < width:
            ratio = height / image_size
            self.image = cv2.resize(self.image, (int(width / ratio), image_size))
            if crop:
                self.image = self.image[0:image_size, 0:image_size]

        elif height > width:
            ratio = width / image_size
            self.image = cv2.resize(self.image, (image_size, int(height / ratio)))
            if crop:
                self.image = self.image[0:image_size, 0:image_size]

        else:
            self.image = cv2.resize(self.image, (image_size, image_size))

        try:
            create_directory(path)
            cv2.imwrite(f"{path}/{self.image_name}", self.image)
            logging.info(f"Saved unplash resized_gt {self.image_name}.")
        except Exception as e:
            logging.error(f"Error while saving unplash resized_gt {self.image_name}. {e}")

    def gaussian_noise(self, sigma):
        """
        Adds gaussian noise to original image and saves it to output_path.
        @param sigma: value of sigma that determines noise intensity
        """
        mean = 0
        result = methods.gaussian(self.image, sigma)
        self.save_result(f"Added gaussian noise with sigma {sigma} and mean {mean} to image {self.image_name}.",
                         result)

    def salt_and_pepper(self, alpha):
        """
        Adds gaussian noise to original image and saves it to output_path.
        @param alpha: value of sigma that determines noise intensity
        """
        result = methods.sp(self.image, alpha)
        self.save_result(f"Added salt & pepper noise with probability {1 - alpha} to image {self.image_name}.",
                         result)

    def median_filter(self, kernel_size):
        """
        Applies median filter to original image and saves it to output_path.
        @param kernel_size: size of filter kernel
        """
        try:
            result = cv2.medianBlur(self.image, kernel_size)
        except Exception as e:
            print(e)
        self.save_result(f"Median filter", result)

    def save_result(self, msg, result):
        """
        Saves image to output_path.
        @param msg: message for logger
        @param result: image to save
        """
        try:
            cv2.imwrite(f"{self.output_path}/{self.image_name}", result)
            logging.info(msg)
        except Exception as e:
            logging.error(f"Error while saving unplash with noise {self.image_name}. {e}")

    def add_rain(self, intensity=None, kernel_size=30, angle=1):
        """
        Adds rain to original image and saves it to output_path.
        @param kernel_size: determines rain drops length
        @param angle: (int) determines drops angle, parameter in range [-3,3] (0 - horizontal, >0 sloping right, <0 sloping left)
        @param intensity: determines rain intensity, if intensity=None then value of intensity is a random number in range from intensity_by_angle_map
        @return image with rain
        """

        if not intensity:
            intensity_by_angle_map = {
                0: [0.005, 0.015],
                1: [0.015, 0.025],
                2: [0.015, 0.025],
                3: [0.04, 0.1]
            }
            intensity = random.uniform(intensity_by_angle_map[abs(angle)][0], intensity_by_angle_map[abs(angle)][1])

        result = methods.rain(self.image, kernel_size, angle, intensity)
        self.save_result(f"Added rain with intensity {intensity}, kernel size {kernel_size} and angle {angle}.", result)

    def remove_rain(self, r, epsilon):
        """
        Removes rain from image and  saves it to output_path.
        @param r: parameter of guided filter
        @param epsilon: parameter of guided filter
        """
        result = methods.remove_rain(self.image, r=r, epsilon=epsilon)
        self.save_result(f"Remove rain", result)


def rms_contrast(filename, input_path, output_path, limit=80):
    """
    Assign image to folder with images with the same rms contrast
    @param filename: image name
    @param input_path: path to folder where image is located
    @param output_path: path to folder with folders with images with the same rms contrast
    @param limit: maximum number od images with the same contrast in one folder

    """
    path = f"{input_path}/{filename}"
    contrast_count = {}
    image = cv2.imread(path, 0) / 255
    mean = cv2.mean(image)[0]
    height, width = image.shape
    result = 0
    for i in range(height):
        for j in range(width):
            result += (image[i][j] - mean) ** 2
    result = round(sqrt(result / (height * width)), 2)
    contrast_count[result] = contrast_count.get(result, 0) + 1
    result_path = f"{output_path}/{result}"
    create_directory(result_path)
    if len(os.listdir(result_path)) < limit:
        shutil_copy(input_path, result_path)


if __name__ == '__main__':
    try:
        input_path, output_path, noise_name = [param for param in input().split()]
        if noise_name=="remove_rain":
            r, epsilon = [param for param in input().split()]
        if noise_name=="median":
            k =input().split()[0]
        files = os.listdir(input_path)
        for file in files:
            try:
                noise = Noise(input_path, output_path, file)
                if noise_name == "sp":
                    noise.salt_and_pepper(alpha=random.uniform(0.01, 0.3))
                elif noise_name == "gaussian":
                    noise.gaussian_noise(sigma=random.uniform(0.01, 0.3))
                elif noise_name == "rain":
                    angle = random.randrange(-3, 3)
                    kernel_size = random.randrange(5, 40)
                    noise.add_rain(angle=angle, kernel_size=kernel_size)
                elif noise_name == "remove_rain":
                    noise.remove_rain(int(r), float(epsilon))
                elif noise_name == "median":
                    noise.median_filter(int(k))
            except Exception as e:
                logging.error(f"Image: {file}.png.{e}")
    except FileNotFoundError as e:
        logging.error(f"Invalid path: {e}")
        print("Podana ścieżka jest niepoprawa")
