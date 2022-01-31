import cv2 as cv
import numpy as np
from . import dct_blur_detector

def get_blur_value(image: np.array):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    fm = cv.Laplacian(gray, cv.CV_64F).var()
    return round(fm, 2)

def get_dct_blur_value(image: np.array):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    dctBlurDetector = dct_blur_detector.BlurDetector(downsampling_factor=4, num_scales=4, scale_start=2, num_iterations_RF_filter=3)
    blur_map = dctBlurDetector.detectBlur(gray)
    normalized_map = (blur_map - np.min(blur_map))/np.ptp(blur_map)
    return np.mean(normalized_map, axis=(0, 1))