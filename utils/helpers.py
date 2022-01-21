import math
import typing
import cv2 as cv
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
    if is_vertical_image(image):
        image = cv.resize(image, (config.processing_height, config.processing_width), interpolation=cv.INTER_CUBIC)
    else:
        image = cv.resize(image, (config.processing_width, config.processing_height), interpolation=cv.INTER_CUBIC)
    cv.imshow('image', image)
    key = cv.waitKey(0)
    if key == ord('q'):
        cv.destroyAllWindows()
    return image
