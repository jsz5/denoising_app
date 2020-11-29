import os

import torch
from PIL import Image
import numpy as np
from torchvision import transforms
from images.neural_network.skip import skip
from images.neural_network.transoformers import GuidedFilterTransform, ToTensor


class Denoising:
    TRAINED_NETWORKS_PATH = "neural_network/trained_networks"

    def __init__(self, image, noise):
        self.activation = "LeakyReLU"
        torch.backends.cudnn.enabled = True
        torch.backends.cudnn.benchmark = True
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dtype = torch.cuda.FloatTensor
        self.image = image
        self.noise = noise
        self.trained_network = self.__get_trained_network()

    def get_net(self):
        return skip(3, 3, num_channels_down=[128] * 5,
                    num_channels_up=[128] * 5,
                    num_channels_skip=[4] * 5,
                    upsample_mode="bilinear",
                    pad='reflection', act_fun=self.activation).type(self.dtype)

    def image_preprocess(self):
        transforms_array = []
        if self.noise == "rain":
            transforms_array.append(GuidedFilterTransform())
        transforms_array.append(ToTensor())
        transform = transforms.Compose(transforms_array)
        transformed_image = transform(self.image)
        transformed_image = torch.from_numpy(transformed_image)
        batch_t = torch.unsqueeze(transformed_image, 0)
        return batch_t

    def denoise(self):
        net = self.get_net()
        net.load_state_dict(torch.load(self.trained_network))
        noisy = self.image_preprocess()
        predicted = net(noisy.to(self.device))
        predicted = predicted.squeeze()
        return transforms.ToPILImage()(predicted.cpu()).convert("RGB")

    def __get_trained_network(self):
        return os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            f"{self.TRAINED_NETWORKS_PATH}/{self.noise}.pth")
