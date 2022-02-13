import re

import numpy as np

from config import config
from utils import calculate_min_max_of_list, min_max_normalize


def get_face_weight(face_sim_data):
    length = len(face_sim_data["face_distance"])
    if face_sim_data["face_match_file"]:
        rank = int(re.split(r"[^a-zA-Z0-9\s]", face_sim_data["face_match_file"])[0])
        face_weight = length - rank + 1
    else:
        return config.default_face_weight
    return face_weight


def calculate_face_coverage_score(face, image_height):
    face_height = face["location"]["x2"] - face["location"]["x1"]
    if face_height > config.face_height_threshold * image_height:
        fcs = face["face_weight"] * float(face_height) / float(image_height)
    else:
        return config.default_face_coverage_score
    return fcs


def calculate_face_score(clusters_data):
    face_dct_list = list()
    face_score = list()
    for cluster in clusters_data:
        for value in cluster.values():
            image_height = value["height"]
            
            for face in value.get("faces", []):
                face_sim_data = face.get("face_similarity")
                if face_sim_data:
                    face["face_weight"] = get_face_weight(face_sim_data)
                else:
                    face["face_weight"] = config.default_face_weight
                face["face_coverage_score"] = calculate_face_coverage_score(face, image_height)
                face_dct_list.append(face["dct_blur"])
            group_emo = get_group_emotion_score(value.get("faces", []))
            image_face_score = 0
            for face in value.get("faces", []):
                emo_score = get_face_cosine_sim(face, group_emo)
                tebb = get_TEBB_score(face["dct_blur"],  get_blink_flag(face), emo_score)
                face["tebb"] = tebb
                image_face_score = image_face_score + tebb
            value["image_face_score"] = image_face_score
            face_score.append(image_face_score)
    face_dct_min, face_dct_max = calculate_min_max_of_list(face_dct_list)
    face_score_min, face_score_max = calculate_min_max_of_list(face_score)
    for cluster in clusters_data:
        for value in cluster.values():
            value["normalized_face_score"] = min_max_normalize(value["image_face_score", face_score_min, face_score_max)
            for face in value.get("faces", []):
                face["normalized_dct_blur"] = min_max_normalize(face["dct_blur"], face_dct_min, face_dct_max)


def get_group_emotion_score(faces):
    sad = 0
    happy = 0
    for face in faces:
        sad = sad + (face["face_weight"] * face["face_feature"]["emotion"]["sad"])
        happy = happy + (face["face_weight"] * face["face_feature"]["emotion"]["happy"])

    return np.array([sad, happy])


def get_face_cosine_sim(face, group_emotion):
    emo = np.array([face["face_feature"]["emotion"]["sad"], face["face_feature"]["emotion"]["happy"]])
    return np.dot(emo, group_emotion) / (np.linalg.norm(emo) * np.linalg.norm(group_emotion))
    

def get_blink_flag(face):
    blink_thresh = 0
    if face["dominant_race"] == "asian":
        blink_thresh = 1
    else:
        blink_thresh = 2
        
    yaw = face["pose"][1]
    pitch = face["pose"][0]
    
    blink_flag = -1
        
    if yaw > 30 or yaw < -30 or pitch > 30 or pitch < -30 or face["face_feature"]["emotion"]["sad"] > 90 or face["face_feature"]["emotion"]["happy"] > 90:
        blink_flag = 1
    else :
        if face["eye_data"]["eye_blink_ratio"] > blink_thresh:
            blink_flag = 1
        else:
            blink_flag = -1
    return blink_flag
    
    
def get_TEBB_score(blur, blink_flag, emotion_score):
    return blur * blink_flag * emotion_score
        