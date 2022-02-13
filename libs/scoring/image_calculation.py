import math

from config import config
from utils import calculate_min_max_of_list, min_max_normalize


def calculate_image_score(clusters_data):
    final_image_score_list = list()
    for cluster in clusters_data:
        image_score_list = list()
        for value in cluster.values():
            value["image_score"] = config.blur_weight * value["normalized_blur_score"] + config.face_weight * value[
                "normalized_face_score"]
            image_score_list.append(value["image_score"])
        z_count = min(1, math.ceil(config.z * len(cluster)))
        image_score_list.sort(reverse=True)
        z_value = image_score_list[z_count - 1]
        for value in cluster.values():
            if value["image_score"] >= z_value:
                gamma = config.z_gamma
            else:
                gamma = config.default_z_gamma
            value["gamma"] = gamma
            value["final_image_score"] = gamma * value["image_score"]
            final_image_score_list.append(value["final_image_score"])
    final_image_score_min, final_image_score_max = calculate_min_max_of_list(final_image_score_list)
    for cluster in clusters_data:
        for value in cluster.values():
            value["absolute_score"] = min_max_normalize(value["final_image_score"], final_image_score_min,
                                                        final_image_score_max)
            stars = math.ceil(value["absolute_score"] / 20)
            value["stars"] = stars
