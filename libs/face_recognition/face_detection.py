import cv2 as cv
import insightface
import numpy as np

from config import config

model = insightface.app.FaceAnalysis()
model.prepare(ctx_id=0)


def get_face_info(image):
    faces = model.get(image)
    return faces


def get_face_images_info(image):
    faces = get_face_info(image)
    if not faces:
        return None
    face_info = list()
    face_locations = list()
    faces_image = list()
    for i, face in enumerate(faces):
        face_location = {"x1": int(face.bbox[1]), "x2": int(face.bbox[3]), "y1": int(face.bbox[0]), "y2":
            int(face.bbox[2])}
        face_img = image[face_location["x1"]:face_location["x2"], face_location["y1"]:face_location["y2"]]
        face_data = dict()
        face_data["landmarks"] = face.landmark_3d_68
        face_data["embedding"] = face.embedding
        if config.image_debug_mode:
            cv.imshow(f'Image Face {i + 1}', face_img)
            _ = cv.waitKey(0)
            cv.destroyAllWindows()
        face_info.append(face_data)
        faces_image.append(face_img)
        face_locations.append(face_location)
    return np.array(face_info), np.array(faces_image), np.array(face_locations)
