import numpy as np


def get_face_distance(known_faces, current_face_encoding):
    if not isinstance(known_faces, list):
        known_faces = np.array([known_faces])
    if current_face_encoding is None:
        return None
    distance = np.linalg.norm(known_faces - current_face_encoding, axis=1)
    return distance
