from deepface import DeepFace
import cv2 as cv


def get_face_feature(image):
    try:
        #print(image)
        image_features = DeepFace.analyze(image, enforce_detection=False)
    except:
        return None
    
    return image_features
