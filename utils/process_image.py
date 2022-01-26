from utils import *
from libs import *


def process_image(image_path):
    image = imread(image_path)
    data = dict()
    data["exposure"] = get_exposure_value(image)
    data["blur"] = get_blur_value(image)
    faces = get_face_images(image)
    data["emotion"] = list()
    for i, face in enumerate(faces):
        emotion = get_emotion(face)
        if emotion:
            del emotion["region"]
            data["emotion"].append(emotion)
    return data
