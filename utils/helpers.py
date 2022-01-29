import math
import typing

import cv2 as cv
import dlib
import imutils
import numpy as np
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


def is_face_present(image):
    face_detector = dlib.get_frontal_face_detector()
    if face_detector(image) or config.advanced_face_recognition:
        return True
    return False


def generate_blur_data(blur_value):
    blur_data = dict()
    blur_data["blur_value"] = blur_value
    if blur_value < config.blur_threshold:
        blur_data["is_blur"] = True
    else:
        blur_data["is_blur"] = False
    return blur_data


def generate_exposure_data(exposure_value):
    exposure_data = dict()
    exposure_data["exposure_value"] = exposure_value
    if exposure_value > config.exposure_threshold_high:
        exposure_data["exposure_status"] = "over_exposed"
    elif exposure_value < config.exposure_threshold_low:
        exposure_data["exposure_status"] = "under_exposed"
    else:
        exposure_data["exposure_status"] = "exposed"
    return exposure_data


def generate_eye_data(eye_status):
    eye_data = dict()
    eye_data["eye_blink_ratio"] = eye_status
    if config.open_eye_threshold_low < eye_status < config.open_eye_threshold_high:
        eye_data["eye_open"] = True
    else:
        eye_data["eye_open"] = False
    return eye_data


def generate_face_similarity_data(face_distance):
    face_similarity = dict()
    face_similarity["face_distance"] = face_distance
    face_match = face_distance <= config.face_similarity_tolerance
    face_similarity["face_match"] = np.any(face_match)
    return face_similarity


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
