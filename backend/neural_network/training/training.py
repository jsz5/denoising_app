import json
import zipfile

import numpy as np
import skimage.measure as ms
import torch
from torch.utils.data import DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter
from torchsummary import summary

from neural_network.config import MSE, DATASET_SIZES_DEFAULT, LEAKY_RELU
from neural_network.data.datasets import NoiseDataset
from neural_network.models.loss_functions import Loss
from neural_network.utils import get_net, prepare_transforms


class EarlyStopping:
    """
    Early stopping for training neural networks
    """

    def __init__(self, loss_percent, patience):
        """
        @param loss_percent: number of percent by which validation loss must decrease for training to stop
        @param patience: number of epochs after which training stops if validation loss doesn't decrease by specified number of percent (loss_percent)
        """
        self.best_loss = None
        self.best_net_dict = None
        self.loss_percent = loss_percent / 100
        self.patience = patience
        self.counter = 0
        self.stopped = False
        self.best_epoch = None

    def check(self, net, validation_loss, epoch):
        """
        Checks if training is to stop
        @param net: trained network
        @param validation_loss: value of validation loss
        @param epoch: number of actual epoch
        """
        if self.best_loss is None:
            self.__new_best(net, validation_loss, epoch)
        elif validation_loss >= (1 - self.loss_percent) * self.best_loss:
            if self.counter > self.patience:
                self.stopped = True
                return
            self.counter += 1
        else:
            self.__new_best(net, validation_loss, epoch)
            self.counter = 0

    def __new_best(self, net, validation_loss, epoch):
        """
        Saves new lowest value of validation loss
        """
        self.best_loss = validation_loss
        self.best_net_dict = net.state_dict()
        self.best_epoch = epoch


class LearningNet:
    def __init__(self, noise_name=None, net=None, special=None, activation=LEAKY_RELU, train_mode=True,
                 data_path=None, dataset_sizes=DATASET_SIZES_DEFAULT):
        """

        @param noise_name: name of noise
        @param net: path to already trained network to test it or train more
        @param special: optional filter applied to noise image (GUIDED_FILTER|MEDIAN_INPUT_ONLY)
        @param activation: name of activation function (LEAKY_RELU|SWISH|MISH)
        @param train_mode: True for training, False for testing
        @param data_path: path to folder with training and testing data wih folders gt - original images and
        noise - images with noise
        @param dataset_sizes: sizes of training, validation and testing dataset
        """
        self.dtype = torch.cuda.FloatTensor
        self.special = special
        self.activation = activation
        self.net = get_net(activation, self.dtype)
        if train_mode:
            self.image_size = 128
            self.noise_name = noise_name
            self.data_path = data_path
            self.__set_params()
            self.dataset_sizes = dataset_sizes
            train_dataloader, val_dataloader, test_dataloader = self.__get_data()
            self.dataloaders = {
                "train": train_dataloader,
                "val": val_dataloader,
                "test": test_dataloader
            }
            self.summary = True
        if net:
            self.net.load_state_dict(torch.load(net))
            self.summary = False

    def __set_params(self):
        """
        Sets initial parameters
        """
        torch.backends.cudnn.enabled = True
        torch.backends.cudnn.benchmark = True
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def __get_data(self):
        """
        @return dataloaders with split training, validation and testing datasets
        """
        transform = prepare_transforms(self.special)
        with zipfile.ZipFile("./drive/My Drive/inżynierska/imagenet_data.zip", 'r') as zip_ref:
            zip_ref.extractall('./noise_remover/data')
        dataset = NoiseDataset(self.data_path, transform=transform)
        train_data, test_data = random_split(dataset, [self.dataset_sizes["train"],
                                                       self.dataset_sizes["val"] + self.dataset_sizes["test"]])
        test_data, val_data = random_split(test_data, [self.dataset_sizes["test"], self.dataset_sizes["val"]])

        train_dataloader = DataLoader(train_data, batch_size=10, shuffle=True, num_workers=16)
        val_dataloader = DataLoader(test_data, batch_size=10, shuffle=True, num_workers=16)
        test_dataloader = DataLoader(val_data, batch_size=10, shuffle=True, num_workers=16)
        return train_dataloader, val_dataloader, test_dataloader

    def train(self, num_epochs, early_stopping, net_path, log_path, start_epoch=0, criterion_name=MSE,
              learning_rate=0.005,
              early_stopping_percentage=2,
              early_stopping_patience=50):
        """

        @param num_epochs: number of epochs the network is trained
        @param early_stopping: determines if training is stopped early
        @param net_path: path to save trained network
        @param log_path: path to save tensorboard logs from training
        @param start_epoch: number of epoch from which training starts
        @param criterion_name: name of loss function (MSE|SSIM|PERCEPTUAL_LOSS)
        @param learning_rate: learning rate of training
        @param early_stopping_percentage: number of percent by which validation loss must decrease for training to stop
        (early_stopping must be True)
        @param early_stopping_patience: number of epochs after which training stops if validation loss doesn't decrease
        early_stopping_percentage percent (early_stopping must be True)

        """
        self.epoch_number = num_epochs
        self.loss_function = criterion_name
        net_name = f"{self.noise_name}_{num_epochs}_{criterion_name}_{self.activation}"
        if self.special:
            net_name = f"{net_name}_{self.special}"

        writer = SummaryWriter(log_dir=log_path,
                               filename_suffix=net_name)
        if self.summary:
            summary(self.net, (3, self.image_size, self.image_size))
        criterion = Loss(criterion_name)
        num_epochs = num_epochs
        optimizer = torch.optim.Adam(self.net.parameters(), lr=learning_rate)
        epoch = start_epoch
        early_stopping_checker = EarlyStopping(loss_percent=early_stopping_percentage, patience=early_stopping_patience)
        while epoch < num_epochs:  # loop over the dataset multiple times
            print(f"Epoch {epoch}/{num_epochs - 1}")
            print('-' * 10)

            for phase in ['train', 'val']:
                if phase == 'train':
                    self.net.train()  # Set model to training mode
                else:
                    self.net.eval()  # Set model to evaluate mode
                running_loss = 0.0
                for i, data in enumerate(self.dataloaders[phase]):
                    ground_truths, noisy = data
                    ground_truths = ground_truths.to(self.device)
                    noisy = noisy.to(self.device)
                    optimizer.zero_grad()
                    outputs = self.net(noisy)
                    loss = criterion.loss(outputs, ground_truths)
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
                    running_loss += loss.item()
                epoch_loss = running_loss / len(self.dataloaders[phase].dataset)
                writer.add_scalar(f"Loss/{phase}", epoch_loss, epoch)
                print(f"{phase} Loss: {epoch_loss}")
                if phase == "val" and early_stopping:
                    early_stopping_checker.check(self.net, epoch_loss, epoch)
                print(f"early_stopping.counter {early_stopping_checker.counter}")
                print(f"early_stopping.best {early_stopping_checker.best_loss}")
            if early_stopping and early_stopping_checker.stopped:
                break
            epoch += 1
        print('Finished Training')
        writer.flush()
        writer.close()
        PATH = f'{net_path}/{early_stopping_checker.best_epoch}_{net_name}.pth'
        torch.save(early_stopping_checker.best_net_dict, PATH)

    def test(self, log_file):
        """
        @param log_file: path to file where average ssim, psnr and mse is calculated
         on original and denoised images from testing dataset

        """
        ssim = []
        psnr = []
        mse = []
        for i, data in enumerate(self.dataloaders["test"], 0):
            ground_truths, noisy = data
            ground_truths = ground_truths.to(self.device)
            noisy = noisy.to(self.device)
            predicted = self.net(noisy)
            for batch in range(10):
                ground_truth_image = ground_truths[batch].detach().cpu().numpy().transpose((1, 2, 0))
                predicted_image = predicted[batch].detach().cpu().numpy().transpose(1, 2, 0)
                ssim.append(ms.compare_ssim(ground_truth_image, predicted_image, multichannel=True))
                psnr.append(ms.compare_psnr(ground_truth_image, predicted_image))
                mse.append(ms.compare_mse(ground_truth_image, predicted_image))

        f = open(log_file, "a")
        f.write(f"Noise type: {self.noise_name}\n")
        f.write(f"Epoch number: {self.epoch_number}\n")
        f.write(f"Activation function {self.activation}\n")
        f.write(f"Loss function {self.loss_function}\n")
        f.write(f"Special {self.special}\n")
        f.write(f"SSIM {np.mean(ssim)}\n")
        f.write(f"PSNR {np.mean(psnr)}\n")
        f.write(f"MSE {np.mean(mse)}\n")
        f.write(f"Datasets {json.dumps(self.dataset_sizes)}\n")
        f.write("\n")
        f.write("\n")
        f.close()
