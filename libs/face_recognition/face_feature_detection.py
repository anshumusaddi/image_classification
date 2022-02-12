from deepface import DeepFace


def get_face_feature(image):
    try:
        image_features = DeepFace.analyze(image, enforce_detection=False)
    except:
        return None
    
    return image_features
