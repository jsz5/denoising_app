import numpy as np
import cv2
import random


def gaussian(image, sigma, mean=0):
    image = image / 255
    # Generate Gaussian noise
    noise = np.random.normal(mean, sigma, image.shape)
    # Superimpose noise and image
    result = image + noise
    # Set more than 1 to 1, and less than 0 to 0
    result = np.clip(result, 0, 1)
    # Restore the gray scale of the picture to 0-255
    return np.uint8(result * 255)


def sp(image, alpha):
    probability = 1 - alpha
    transposed_img = image.transpose(2, 1, 0)  # grupujemy każdy kolor
    channels, height, width = transposed_img.shape
    mask = np.random.choice(("real", "salt", "pepper"), size=(1, height, width),
                            p=[probability, (1 - probability) / 2., (1 - probability) / 2.])
    mask = np.repeat(mask, channels, axis=0)  # kopiujemy dla każdego kanału, żeby miało rozmiar obrazu
    transposed_img[mask == "salt"] = 255  # salt and pepper na każdym kolorze r,g,b
    transposed_img[mask == "pepper"] = 0  #
    return np.uint8(transposed_img.transpose(2, 1, 0))


def rain(image, kernel_size, angle, intensity=None):
    """
         Parameters
         ----------
         intensity : float
             Rain intensity
         kernel_size:int
             Drops length
         angle: int
             Rain angle (0 - horizontal, >0 sloping, <0 sloping to the other side)

         ----------
         intensity_by_angle_map - for angle 0 -> 0.002<=intensity<= 0.015
         """

    angle_param = angle
    if angle < 0:
        angle_param *= (-1)

    if not intensity:
        intensity_by_angle_map = {
            0: [0.005, 0.015],
            1: [0.015, 0.025],
            2: [0.015, 0.025],
            3: [0.04, 0.1]
        }
        intensity = random.uniform(intensity_by_angle_map[angle_param][0], intensity_by_angle_map[angle_param][1])

    image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
    n_channels = 4
    img = np.zeros((image.shape[0], image.shape[1], n_channels), dtype=np.uint8)
    # Generate Gaussian noise mean (0)
    noise = np.random.uniform(0, 255, (image.shape[0], image.shape[1], 1))

    # Rain intensity
    for i, x in enumerate(img):
        for j, y in enumerate(x):
            if np.random.uniform() <= intensity:
                img[i][j] = noise[i][j]

    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = gamma_correction(0.8, img)

    # Rain slope
    kernel = np.zeros((kernel_size, kernel_size))
    if angle > 0:
        for i in range(kernel.shape[0]):
            for j in range(kernel.shape[1]):
                if j == angle * i:
                    kernel[i][j] = 1

    elif angle < 0:
        param = kernel.shape[1] - 1
        for i in range(kernel.shape[0]):
            for j in range(kernel.shape[1]):
                if j == param:
                    kernel[i][j] = 1
            param -= angle_param
    else:
        kernel[:, int((kernel_size - 1) / 2)] = np.ones(kernel_size)

    kernel /= kernel_size
    filter_img = cv2.filter2D(img, -1, kernel)
    crop_img = filter_img[0:image.shape[0], ]
    result = cv2.add(image, crop_img)
    return np.uint8(cv2.cvtColor(result, cv2.COLOR_RGBA2RGB))


def gamma_correction(gamma, image):
    look_up = np.empty((1, 256), np.uint8)
    for i in range(256):
        look_up[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    return cv2.LUT(image, look_up)


def contrast_and_brightness(image, alpha, beta):
    image = np.array(image).astype(int)
    image = np.clip(alpha * image + beta,0, 255)
    return image


def color_balance(image, blue, green, red):
    print(blue)
    print(green)
    print(red)
    result = np.zeros(image.shape)
    result[:, :, 0] = ((1 + 2 * blue) * image[:, :, 0] + (1 - green) * image[:, :, 1] + (1 - red) * image[:, :, 2]) / 3
    result[:, :, 1] = ((1 + 2 * green) * image[:, :, 1] + (1 - blue) * image[:, :, 0] + (1 - red) * image[:, :, 2]) / 3
    result[:, :, 2] = ((1 + 2 * red) * image[:, :, 2] + (1 - blue) * image[:, :, 0] + (1 - green) * image[:, :, 1]) / 3
    # result = result / 255
    print(result)
    return result

def remove_rain(rain_image, r, epsilon):
    low_frequency = np.empty(rain_image.shape)
    new_high_frequency = np.empty(rain_image.shape)
    result = np.empty(rain_image.shape)
    epsilon = epsilon ** 2
    epsilon *= 255 ** 2
    guided_filter = cv2.ximgproc.createGuidedFilter(rain_image, r, epsilon)
    low_frequency = guided_filter.filter(rain_image, low_frequency)
    high_frequency = cv2.subtract(rain_image, low_frequency)
    laplacian = cv2.Laplacian(low_frequency, cv2.CV_64F, ksize=1)
    laplacian = np.absolute(laplacian)
    laplacian = np.uint8(laplacian)
    low_edges = cv2.addWeighted(low_frequency, 1, laplacian, 0.1, 0)
    guided_filter2 = cv2.ximgproc.createGuidedFilter(low_edges, r, epsilon)
    new_high_frequency = guided_filter2.filter(high_frequency, new_high_frequency)
    recovered = cv2.add(low_edges, new_high_frequency)
    cleared = np.minimum(recovered, rain_image)
    b = 0.5
    refined = (b * cleared) + ((1 - b) * recovered)
    refined = np.uint8(refined)
    guided_filter3 = cv2.ximgproc.createGuidedFilter(refined, r, epsilon)
    result = guided_filter3.filter(cleared, result)
    return result
