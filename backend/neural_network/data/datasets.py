import os

from skimage import io
from torch.utils.data.dataset import Dataset


class NoiseDataset(Dataset):
    """
    Creates torch dataset from files
    """

    def __init__(self, main_path: str, transform):
        """

        @param main_path (str):  Path to folder with original and noise images. Original images are in folder 'gt', noise images are in folder 'noise'
        @param transform: Transform operations applied to images

        """
        ## Path to folder with original images
        self.gt_path = f"{main_path}/gt"
        ## Path to folder with images with noise
        self.noise_path = f"{main_path}/noise"
        ##List of original images' names
        self.images_list = os.listdir(self.gt_path)
        ##Object of transforms.Compose to transform images
        self.transform = transform

    def __len__(self):
        """
        @return Length of dataset
        """
        return len(self.images_list)

    def __getitem__(self, idx):
        """
        @param idx: Index of sample of images: original and with noise
        @return (tuple) Transformed tuple of original image and image with noise
        """
        img_name = os.path.join(self.gt_path, self.images_list[idx])
        noise_img_name = os.path.join(self.noise_path, self.images_list[idx])
        image = io.imread(img_name)
        noise_image = io.imread(noise_img_name)
        sample = self.transform((image, noise_image))
        return sample
