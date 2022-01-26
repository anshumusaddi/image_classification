import face_recognition
import cv2 as cv
import numpy as np
from config import config


def get_faces(image):
    faces = face_recognition.face_locations(image)
    return faces


def get_face_images(image):
    faces = get_faces(image)
    if not faces:
        return None
    faces_image = list()
    for i, face in enumerate(faces):
        face_img = image[face[0]:face[2], face[3]:face[1]]
        if config.image_debug_mode:
            cv.imshow(f'Image Face {i+1}', face_img)
            _ = cv.waitKey(0)
            cv.destroyAllWindows()
        faces_image.append(face_img)
    return np.array(faces_image)
