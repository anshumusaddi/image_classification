from libs import *


def process_face(image, known_faces=None, location=None):
    data = dict()
    face_present = is_face_present(image)
    if not face_present:
        return data
    face_feature = get_face_feature(image)
    data["dct_blur"] = get_dct_blur_value(image)
    if face_feature:
        del face_feature["region"]
        data["face_feature"] = face_feature
    eye_status = get_eye_open_status(image)
    if eye_status:
        data["eye_data"] = generate_eye_data(eye_status)
    if known_faces:
        face_similarity_list = get_face_distance(list(known_faces.values()), image)
        if face_similarity_list is not None:
            data["face_similarity"] = generate_face_similarity_data(face_similarity_list, list(known_faces.keys()))
    if location and data:
        data["location"] = location
    return data


def process_image(image, known_faces=None):
    data = dict()
    blur_value = get_blur_value(image)
    data["blur"] = generate_blur_data(blur_value)
    exposure_value = get_exposure_value(image)
    data["exposure"] = generate_exposure_data(exposure_value)
    data["sharpness"] = get_sharpness_value(image)
    face_images, face_locations = get_face_images(image)
    face_data_list = list()
    for face, location in zip(face_images, face_locations):
        face_data = process_face(face, known_faces, location)
        if face_data:
            face_data_list.append(face_data)
    if face_data_list:
        data["faces"] = face_data_list
    return data


def load_known_images(file_path):
    images = glob(os.path.join(file_path, '*'))
    known_face_encoding = dict()
    for image_path in images:
        image = imread(image_path)
        face_images, _ = get_face_images(image)
        face_image = face_images[0]
        face_encoding = get_face_encoding(face_image)
        if face_encoding is not None:
            known_face_encoding[os.path.basename(image_path)] = face_encoding
    return known_face_encoding
