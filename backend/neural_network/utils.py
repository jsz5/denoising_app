from torchvision import transforms

from neural_network.config import MEDIAN_INPUT_ONLY, GUIDED_FILTER
from neural_network.data.transoformers import ToTensor, MedianFilterTransform, GuidedFilterTransform
from neural_network.models.skip import skip


def get_net(activation, dtype):
    """
    @param activation: activation function name
    @return neural network with used parameters
    """
    return skip(3, 3, num_channels_down=[128] * 5,
                num_channels_up=[128] * 5,
                num_channels_skip=[4] * 5,
                upsample_mode="bilinear",
                pad='reflection', act_fun=activation).type(dtype)


def prepare_transforms(special):
    """
    @param special: determines if images are to be preprocessed (MEDIAN_INPUT_ONLY|GUIDED_FILTER)
    @return transforms
    """
    transforms_array = []
    if special == MEDIAN_INPUT_ONLY:
        transforms_array.append(MedianFilterTransform())
    if special == GUIDED_FILTER:
        transforms_array.append(GuidedFilterTransform())
    transforms_array.append(ToTensor())
    transform = transforms.Compose(transforms_array)
    return transform
