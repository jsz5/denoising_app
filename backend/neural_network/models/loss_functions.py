import torch
from pytorch_msssim import ssim, ms_ssim, SSIM, MS_SSIM

from .vgg import Vgg16
from neural_network.config import PERCEPTUAL_LOSS


class Loss:
    """
    Calculates loss function in training

    """

    CONTENT_WEIGHT = 1 #weight constant in perceptual loss
    TV_WEIGHT = 1e-7 #weight constant of total variation regularization in perceptual loss

    def __init__(self, loss_function_name):
        """
        @param loss_function_name: type of loss function
        """
        self.loss_function_name = loss_function_name
        if loss_function_name == PERCEPTUAL_LOSS:
            self.vgg = Vgg16().type(torch.cuda.FloatTensor)
        else:
            self.loss_function = getattr(self, loss_function_name)()

    def loss(self, outputs, gt):
        """
        @param outputs: batch with denoised images
        @param gt:  batch with original images
        @return loss function value between denoised and original images
        """
        if self.loss_function_name == PERCEPTUAL_LOSS:
            return self.perceptual_loss(outputs, gt)
        return getattr(self, f"{self.loss_function_name}_loss")(self.loss_function(outputs, gt))

    def mse(self):
        """
        @return mse function
        """
        return torch.nn.MSELoss()

    def mse_loss(self, loss_function_value):
        """
        @param loss_function_value: mse value between denoised and original images
        @return mse loss function between denoised and original images
        """
        return loss_function_value

    def ssim(self):
        """
         @return ssim function on normalized image with 3 channels
        """
        return SSIM(data_range=1, size_average=True, channel=3)

    def ssim_loss(self, loss_function_value):
        """
        @param loss_function_value: ssim value between denoised and original images
        @return ssim loss function between denoised and original images
        """
        return 1 - loss_function_value

    def perceptual_loss(self, outputs, ground_truths):
        """
        Calculates perceptual loss function as content loss from vgg16 layer (h_relu_2_2) and tv_loss - total variation regularization
        @param outputs: batch with denoised images
        @param ground_truths: batch with original images
        @return  percepual loss value between denoised and original images
        """
        gt_features = self.vgg(ground_truths)
        outputs_features = self.vgg(outputs)
        # calculate content loss from vgg layer (h_relu_2_2)
        content_loss = self.CONTENT_WEIGHT * self.mse()(gt_features[1], outputs_features[1])

        # calculate total variation regularization
        diff_i = torch.sum(torch.abs(outputs[:, :, :, 1:] - outputs[:, :, :, :-1]))
        diff_j = torch.sum(torch.abs(outputs[:, :, 1:, :] - outputs[:, :, :-1, :]))
        tv_loss = self.TV_WEIGHT * (diff_i + diff_j)
        loss = content_loss + tv_loss

        return loss
