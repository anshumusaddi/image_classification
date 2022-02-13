from utils import calculate_min_max_of_list, min_max_normalize


def calculate_crisp_metric(crisp, dct, sharpness):
    return crisp + dct + sharpness


def calculate_blur_score(clusters_data):
    crisp_list = list()
    dct_list = list()
    sharpness_list = list()
    for cluster in clusters_data:
        for value in cluster.values():
            crisp_list.append(value["blur"]["blur_value"])
            dct_list.append(value["dct_blur"])
            sharpness_list.append(value["sharpness"])

    crisp_min, crisp_max = calculate_min_max_of_list(crisp_list)
    dct_min, dct_max = calculate_min_max_of_list(dct_list)
    sharpness_min, sharpness_max = calculate_min_max_of_list(sharpness_list)

    norm_crisp_list = [min_max_normalize(i, crisp_min, crisp_max) for i in crisp_list]
    norm_dct_list = [min_max_normalize(i, dct_min, dct_max) for i in dct_list]
    norm_sharpness_list = [min_max_normalize(i, sharpness_min, sharpness_max) for i in sharpness_list]
    crisp_metric_list = [calculate_crisp_metric(i, j, k) for i, j, k in zip(norm_crisp_list, norm_dct_list,
                                                                            norm_sharpness_list)]
    crisp_metric_min, crisp_metric_max = calculate_min_max_of_list(crisp_metric_list)

    for cluster in clusters_data:
        for value in cluster.values():
            value["normalized_crisp"] = min_max_normalize(value["blur"]["blur_value"], crisp_min, crisp_max)
            value["normalized_dct"] = min_max_normalize(value["dct_blur"], dct_min, dct_max)
            value["normalized_sharpness"] = min_max_normalize(value["sharpness"], sharpness_min, sharpness_max)
            value["crisp_metric"] = calculate_crisp_metric(value["normalized_crisp"], value["normalized_dct"],
                                                           value["normalized_sharpness"])
            value["normalized_crisp_metric"] = min_max_normalize(value["crisp_metric"], crisp_metric_min,
                                                                 crisp_metric_max)
