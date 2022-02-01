from deepface import DeepFace

from config import config


def get_face_feature(image):
    try:
        image_features = DeepFace.analyze(image, enforce_detection=not config.advanced_face_recognition,
                                          detector_backend='dlib')
    except ValueError:
        return None
    return image_features
