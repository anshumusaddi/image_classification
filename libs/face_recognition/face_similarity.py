import face_recognition

from libs.face_recognition import get_face_encoding


def get_face_distance(known_faces, current_face):
    if not isinstance(known_faces, list):
        known_faces = [known_faces]
    current_face_encoding = get_face_encoding(current_face)
    if current_face_encoding is None:
        return None
    distance = face_recognition.face_distance(known_faces, current_face_encoding)
    return distance
