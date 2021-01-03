import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from neural_network import config

"""
 @file common.py code has been written in project Deep image prior (https://github.com/DmitryUlyanov/deep-image-prior)
 @file skip.py code has been written in project Deep image prior (https://github.com/DmitryUlyanov/deep-image-prior)
"""


def add_module(self, module):
    self.add_module(str(len(self) + 1), module)


torch.nn.Module.add = add_module


class Concat(nn.Module):
    """
    Concatenation of layers in skip connections in the network
    """

    def __init__(self, dim, *args):
        super(Concat, self).__init__()
        self.dim = dim

        for idx, module in enumerate(args):
            self.add_module(str(idx), module)

    def forward(self, input):
        inputs = []
        for module in self._modules.values():
            inputs.append(module(input))

        inputs_shapes2 = [x.shape[2] for x in inputs]
        inputs_shapes3 = [x.shape[3] for x in inputs]

        if np.all(np.array(inputs_shapes2) == min(inputs_shapes2)) and np.all(
                np.array(inputs_shapes3) == min(inputs_shapes3)):
            inputs_ = inputs
        else:
            target_shape2 = min(inputs_shapes2)
            target_shape3 = min(inputs_shapes3)

            inputs_ = []
            for inp in inputs:
                diff2 = (inp.size(2) - target_shape2) // 2
                diff3 = (inp.size(3) - target_shape3) // 2
                inputs_.append(inp[:, :, diff2: diff2 + target_shape2, diff3:diff3 + target_shape3])

        return torch.cat(inputs_, dim=self.dim)

    def __len__(self):
        return len(self._modules)


class Mish(nn.Module):
    """
    Mish function layer
    """

    def forward(self, input):
        return input * torch.tanh(F.softplus(input))


class Swish(nn.Module):
    """
    Swish function layer
    """

    def __init__(self):
        super(Swish, self).__init__()
        self.s = nn.Sigmoid()

    def forward(self, x):
        return x * self.s(x)


def act(act_fun=config.LEAKY_RELU):
    """
    @param act_fun: name of activation function
    @return (str) activation function

    """
    if act_fun == config.LEAKY_RELU:
        return nn.LeakyReLU(0.2, inplace=True)
    elif act_fun == config.SWISH:
        return Swish()
    elif act_fun == config.MISH:
        return Mish()
    else:
        assert False


def bn(num_features):
    """

    @param num_features: number of features
    @return batch normalization layer
    """
    return nn.BatchNorm2d(num_features)


def conv(in_f, out_f, kernel_size, stride=1, bias=True, pad='zero'):
    """
    @param in_f: number of channels in the input image
    @param out_f: number of channels after convolution
    @param kernel_size: size of the convolving kernel
    @param stride: stride of the convolution
    @param bias: adds a learnable bias to the output
    @param pad: determines padding type (zero or reflection)
    @return convolutional layer with optional reflection padding
    """
    padder = None
    to_pad = int((kernel_size - 1) / 2)
    if pad == 'reflection':
        padder = nn.ReflectionPad2d(to_pad)
        to_pad = 0

    convolver = nn.Conv2d(in_f, out_f, kernel_size, stride, padding=to_pad, bias=bias)
    layers = filter(lambda x: x is not None, [padder, convolver])
    return nn.Sequential(*layers)
