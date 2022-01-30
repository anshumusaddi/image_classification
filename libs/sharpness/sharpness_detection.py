import cpbd
import numpy as np


def get_sharpness_value(image: np.array):
    sharpness = cpbd.compute(image)
    print(sharpness)
    return sharpness
