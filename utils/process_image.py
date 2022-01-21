from utils import *
from libs import *


def process_image(image_path):
    image = imread(image_path)
    data = dict()
    data["exposure"] = get_exposure_value(image)
    data["blur"] = get_blur_value(image)
    return data
