import json
import os


class Config(object):
    def __init__(self):
        config_file = os.getenv("CONFIG_FILE", "")
        file_config = dict()
        if config_file:
            with open(config_file) as fp:
                file_config = json.load(fp)

        self.processing_height = file_config.get("processing_height", 640)
        self.image_debug_mode = file_config.get("image_debug_mode", False)
        self.disable_resize = file_config.get("disable_resize", False)
        self.left_eye_landmarks = file_config.get("left_eye_landmarks", [36, 37, 38, 39, 40, 41])
        self.right_eye_landmarks = file_config.get("right_eye_landmarks", [42, 43, 44, 45, 46, 47])
        self.supported_file_formats = file_config.get("supported_file_formats", ['JPEG', 'PNG', 'BMP', 'MPO', 'PPM',
                                                                                 'TIFF', 'GIF'])
        self.similarity_threshold = file_config.get("similarity_threshold", 0.85)

        self.blur_threshold = file_config.get("blur_threshold", 45)
        self.exposure_threshold_low = file_config.get("exposure_threshold_low", 22)
        self.exposure_threshold_high = file_config.get("exposure_threshold_high", 80)
        # eye ratio -> close eyes 2.8 half close 2.7 full open 1.7 normal open 1.12
        self.open_eye_threshold_low = file_config.get("open_eye_threshold_low", 1.5)
        self.open_eye_threshold_high = file_config.get("open_eye_threshold_high", 3)
        self.face_similarity_tolerance = file_config.get("face_similarity_tolerance", 0.5)

        self.default_face_weight = file_config.get("default_face_weight", 0.01)
        self.face_height_threshold = file_config.get("face_height_threshold", 0.1)
        self.default_face_coverage_score = file_config.get("default_face_coverage_score", 0.01)
        self.blur_weight = file_config.get("blur_weight", 0.5)
        self.face_weight = file_config.get("face_weight", 0.5)
        self.z = file_config.get("z", 0.1)
        self.z_gamma = file_config.get("z_gamma", 1)
        self.default_z_gamma = file_config.get("default_z_gamma", 0.1)
        self.thread_count = file_config.get("thread_count", max(os.cpu_count() - 2, 2))


config = Config()
