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
    emo = np.array([face["face_feature"]["emotion"]["sad"], face["face_feature"]["emotion"]["happy"]])
    return np.dot(emo, groupEmotion)/(np.linalg.norm(emo)*np.linalg.norm(groupEmotion))
    

def get_blink_flag(face):
    blink_thresh = 0
    if face["dominant_race"] == "asian":
        blink_thresh = 1
    else:
        blink_thresh = 2
        
    yaw = face["pose"][1]
    pitch = face["pose"][0]
    
    blink_flag = -1
        
    if yaw > 30 or yaw < -30:
        blink_flag = 1
    if pitch > 30 or pitch < -30:
        blink_flag = 1
        
    if face["face_feature"]["emotion"]["sad"] > 90 or face["face_feature"]["emotion"]["happy"] > 90:
        blink_flag = 1
    else :
        if face["eye_data"]["eye_blink_ratio"] > blink_thresh:
            blink_flag = 1
        else:
            blink_flag = -1
    return blink_flag
        