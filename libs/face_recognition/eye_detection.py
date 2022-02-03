from utils import *


def get_blink_ratio(eyes_points, landmark):
    left_corner = (landmark[eyes_points[0]][0], landmark[eyes_points[0]][1])
    right_corner = (landmark[eyes_points[3]][0], landmark[eyes_points[3]][1])

    center_top = mid_point(landmark[eyes_points[1]], landmark[eyes_points[2]])
    center_bottom = mid_point(landmark[eyes_points[4]], landmark[eyes_points[5]])

    vertical_distance = euclidean_distance(center_top, center_bottom)
    horizontal_distance = euclidean_distance(left_corner, right_corner)
    if vertical_distance > 0:
        ratio = horizontal_distance / vertical_distance
    else:
        ratio = None
    return ratio


def get_eye_open_status(image_landmarks):
    left_eye_landmarks = config.left_eye_landmarks
    right_eye_landmarks = config.right_eye_landmarks
    left_blink_ratio = get_blink_ratio(left_eye_landmarks, image_landmarks)
    right_blink_ratio = get_blink_ratio(right_eye_landmarks, image_landmarks)
    if left_blink_ratio and right_blink_ratio:
        blink_ratio = (left_blink_ratio + right_blink_ratio) / 2
    else:
        blink_ratio = None
    return blink_ratio
