import libs.cpbd as cpbd
import numpy as np
import cv2 as cv


def get_sharpness_value(image: np.array):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    sharpness = cpbd.compute(gray)
    return sharpness
