import os

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

from images.config import NET_PATHS
from neural_network.config import LEAKY_RELU
from neural_network.utils import get_net, prepare_transforms


class Denoising:
    def __init__(self, image, noise=None, activation=LEAKY_RELU, special=None, net_path=None):
        """
        @param image: image with noise
        @param noise: noise type
        """
        self.activation = activation
        self.special = special
        torch.backends.cudnn.enabled = True
        torch.backends.cudnn.benchmark = True
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dtype = torch.cuda.FloatTensor
        self.image = Image.open(image).convert('RGB')
        self.noise = noise
        if net_path is None:
            self.trained_network = self.__get_trained_network()
        else:
            self.trained_network = net_path

    def image_preprocess(self):
        """
        @return transformed tensor image
        """
        transform = prepare_transforms(self.special)
        transformed_image = transform(np.array(self.image))
        transformed_image = torch.from_numpy(transformed_image)
        batch_t = torch.unsqueeze(transformed_image, 0)
        return batch_t

    def denoise(self):
        """
        @return denoised image after processing by trained neural network
        """
        net = get_net(self.activation, self.dtype)
        net.load_state_dict(torch.load(self.trained_network))
        noisy = self.image_preprocess()
        predicted = net(noisy.to(self.device))
        predicted = predicted.squeeze()
        return transforms.ToPILImage()(predicted.cpu()).convert("RGB")

    def __get_trained_network(self):
        """
        @return path to neural network used in web app by noise name
        """
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), NET_PATHS[self.noise])
