import os
from glob import glob

from libs import get_face_feature, get_dct_blur_value, get_eye_open_status, get_face_distance, get_blur_value, \
    get_exposure_value, get_sharpness_value, get_face_images_info
from utils.helpers import generate_eye_data, generate_face_similarity_data, generate_blur_data, \
    generate_exposure_data, imread


def process_face(face_info, image, known_faces=None, location=None):
    data = dict()
    face_feature = get_face_feature(image)
    if face_feature:
        del face_feature["region"]
        data["face_feature"] = face_feature
    else:
        return None
    data["dct_blur"] = get_dct_blur_value(image)
    
    eye_status = get_eye_open_status(face_info["landmarks"])
    if eye_status:
        data["eye_data"] = generate_eye_data(eye_status)
    if known_faces:
        face_similarity_list = get_face_distance(list(known_faces.values()), face_info["embedding"])
        if face_similarity_list is not None:
            data["face_similarity"] = generate_face_similarity_data(face_similarity_list, list(known_faces.keys()))
    if location and data:
        data["location"] = location
    data["pose"] = face_info["pose"].tolist()
    return data


def process_image(image, known_faces=None):
    data = dict()
    # fp = open(f"timing/{datetime.now().isoformat()}.txt", "w")
    # fp.write(f"{datetime.now().isoformat()} : Start Time\n")
    blur_value = get_blur_value(image)
    # fp.write(f"{datetime.now().isoformat()} : Normal Blur Time\n")
    data["height"] = image.shape[0]
    data["width"] = image.shape[1]
    data["blur"] = generate_blur_data(blur_value)
    exposure_value = get_exposure_value(image)
    # fp.write(f"{datetime.now().isoformat()} : Exposure Time\n")
    data["exposure"] = generate_exposure_data(exposure_value)
    data["sharpness"] = get_sharpness_value(image)
    # fp.write(f"{datetime.now().isoformat()} : Sharpness Time\n")
    # data["dct_blur"] = get_dct_blur_value(image)
    # fp.write(f"{datetime.now().isoformat()} : DCT Time\n")
    face_infos, face_images, face_locations = get_face_images_info(image)
    # fp.write(f"{datetime.now().isoformat()} : Face Info Time\n")
    face_data_list = list()
    for face_info, face, location in zip(face_infos, face_images, face_locations):
        if face is None or len(face) == 0:
            continue
        face_data = process_face(face_info, face, known_faces, location)
        if face_data:
            face_data_list.append(face_data)
    if face_data_list:
        data["faces"] = face_data_list
    # fp.write(f"{datetime.now().isoformat()} : Face Process Time\n")
    # fp.close()
    return data


def load_known_images(file_path):
    images = glob(os.path.join(file_path, '*'))
    known_face_encoding = dict()
    for image_path in images:
        image = imread(image_path)
        face_info, _, _ = get_face_images_info(image)
        face_info = face_info[0]
        face_encoding = face_info["embedding"]
        if face_encoding is not None:
            known_face_encoding[os.path.basename(image_path)] = face_encoding
    return known_face_encoding
