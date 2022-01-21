import cv2 as cv
import numpy as np


def get_blur_value(image: np.array):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    fm = cv.Laplacian(gray, cv.CV_64F).var()
    return round(fm, 2)
