import cv2 as cv
import dlib
import face_recognition
import numpy as np

from config import config


def get_face_locations(image):
    faces = face_recognition.face_locations(image, model="cnn" if config.advanced_face_recognition else "hog")
    return faces


def get_face_images(image):
    faces = get_face_locations(image)
    if not faces:
        return None
    face_locations = list()
    faces_image = list()
    for i, face in enumerate(faces):
        face_img = image[face[0]:face[2], face[3]:face[1]]
        face_location = {"x1": face[0], "x2": face[2], "y1": face[3], "y2": face[1]}
        if config.image_debug_mode:
            cv.imshow(f'Image Face {i + 1}', face_img)
            _ = cv.waitKey(0)
            cv.destroyAllWindows()
        faces_image.append(face_img)
        face_locations.append(face_location)
    return np.array(faces_image), np.array(face_locations)


def get_face_encoding(image):
    image_encoding = face_recognition.face_encodings(image)
    if not image_encoding:
        return None
    return image_encoding[0]


def get_face_landmarks(image: np.array):
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    predictor = dlib.shape_predictor(config.landmark_model)
    x2, y2 = gray_image.shape
    dlib_rect = dlib.rectangle(0, 0, x2, y2)
    landmarks = predictor(gray_image, dlib_rect)
    return landmarks
