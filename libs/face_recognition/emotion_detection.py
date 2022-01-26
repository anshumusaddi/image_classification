from deepface import DeepFace


def get_emotion(image):
    try:
        image_features = DeepFace.analyze(image, actions=tuple(['emotion']), detector_backend='dlib')
    except ValueError:
        return None
    return image_features
