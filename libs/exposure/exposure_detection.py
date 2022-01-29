import cv2 as cv
import numpy as np


def get_exposure_value(image: np.array):
    hsv_image = cv.mean(cv.cvtColor(image, cv.COLOR_BGR2HSV))
    value = hsv_image[2] / 255 * 100
    return round(value, 2)
