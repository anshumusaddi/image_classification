import math
import typing
import cv2 as cv
import imutils
import rawpy
from config import config


def mid_point(point1, point2):
    midpoint = (int((point1.x + point2.y) / 2), int((point1.x + point2.y) / 2))
    return midpoint


def euclidean_distance(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)


def is_vertical_image(image):
    shape = image.shape
    if shape[0] > shape[1]:
        return True


def imread(path: typing.AnyStr):
    extension = path.split(".")[-1]
    if extension in ["bmp", "pbm", "pgm", "ppm", "sr", "ras", "jpeg", "jpg", "jpe", "jp2", "tiff", "tif", "png"]:
        image = cv.imread(path)
    else:
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess()
        image = cv.cvtColor(rgb, cv.COLOR_RGB2BGR)
    if not config.disable_resize:
        if is_vertical_image(image):
            image = imutils.resize(image, width=config.processing_height)
        else:
            image = imutils.resize(image, width=config.processing_width)
    if config.image_debug_mode:
        cv.imshow('Input Re-Sized Image', image)
        _ = cv.waitKey(0)
        cv.destroyAllWindows()
    return image
