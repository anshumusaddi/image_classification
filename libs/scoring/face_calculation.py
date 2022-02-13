from utils import calculate_min_max_of_list, min_max_normalize
import numpy as np


def get_group_emotion_score(faces):
    
    sad = 0
    happy = 0
    for face in faces:
        sad = sad + (face["face_weight"] * face["face_feature"]["emotion"]["sad"])
        happy = happy + (face["face_weight"] * face["face_feature"]["emotion"]["happy"])

    return np.array([sad, happy])
    

def get_face_cosine_sim(face, groupEmotion):
    emo = np.array([face["face_feature"]["emotion"]["sad"]), face["face_feature"]["emotion"]["happy"])])
    return np.dot(emo, groupEmotion)/(np.linalg.norm(emo)*np.linalg.norm(groupEmotion))