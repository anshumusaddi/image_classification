from libs import calculate_blur_score, calculate_face_score


def process_score(directory_data):
    calculate_blur_score(directory_data)
    calculate_face_score(directory_data)
