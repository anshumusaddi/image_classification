from config import config
from libs.face_recognition.face_detection import get_face_landmarks
from utils import *


def get_blink_ratio(eyes_points, landmark):
    left_corner = (landmark.part(eyes_points[0]).x, landmark.part(eyes_points[0]).y)
    right_corner = (landmark.part(eyes_points[3]).x, landmark.part(eyes_points[3]).y)

    center_top = mid_point(landmark.part(eyes_points[1]), landmark.part(eyes_points[2]))
    center_bottom = mid_point(landmark.part(eyes_points[4]), landmark.part(eyes_points[5]))

    vertical_distance = euclidean_distance(center_top, center_bottom)
    horizontal_distance = euclidean_distance(left_corner, right_corner)
    if vertical_distance > 0:
        ratio = horizontal_distance / vertical_distance
    else:
        ratio = None
    return ratio


def get_eye_open_status(image):
    left_eye_landmarks = config.left_eye_landmarks
    right_eye_landmarks = config.right_eye_landmarks
    image_landmarks = get_face_landmarks(image)
    left_blink_ratio = get_blink_ratio(left_eye_landmarks, image_landmarks)
    right_blink_ratio = get_blink_ratio(right_eye_landmarks, image_landmarks)
    if left_blink_ratio and right_blink_ratio:
        blink_ratio = (left_blink_ratio + right_blink_ratio) / 2
    else:
        blink_ratio = None
    return blink_ratio
