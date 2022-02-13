import math
import typing

import cv2 as cv
import imutils
import numpy as np

from config import config


def mid_point(point1, point2):
    midpoint = (int((point1[0] + point2[1]) / 2), int((point1[0] + point2[1]) / 2))
    return midpoint


def euclidean_distance(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)


def is_vertical_image(image):
    shape = image.shape
    if shape[0] > shape[1]:
        return True


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


def generate_face_similarity_data(face_distance, file_names):
    face_similarity = dict()
    face_similarity["face_distance"] = face_distance.tolist()
    face_match = face_distance <= config.face_similarity_tolerance
    match_name = None
    match_min = None
    for match in np.where(face_match)[0]:
        if match_min is None or match_min > face_distance[match]:
            match_min = face_distance.tolist()[match]
            match_name = file_names[match]
    face_similarity["face_match_file"] = match_name
    return face_similarity


def imread(path: typing.AnyStr):
    extension = path.split(".")[-1]
    if extension.lower() in ["bmp", "pbm", "pgm", "ppm", "sr", "ras", "jpeg", "jpg", "jpe", "jp2", "tiff", "tif",
                             "png"]:
        image = cv.imread(path)
    else:
        # with rawpy.imread(path) as raw:
        #     rgb = raw.postprocess()
        # image = cv.cvtColor(rgb, cv.COLOR_RGB2BGR)
        raise ValueError(f"{extension} Not Supported Yet!")
    if not config.disable_resize:
        if is_vertical_image(image):
            image = imutils.resize(image, width=config.processing_height)
        else:
            image = imutils.resize(image, height=config.processing_height)
    if config.image_debug_mode:
        cv.imshow('Input Re-Sized Image', image)
        _ = cv.waitKey(0)
        cv.destroyAllWindows()
    return image


def calculate_min_max_of_list(input_list: typing.List):
    min_list = min(input_list)
    max_list = max(input_list)
    return min_list, max_list


def min_max_normalize(value, minimum, maximum):
    return (value - minimum) / (maximum - minimum) * 100
