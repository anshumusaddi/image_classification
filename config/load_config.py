import json
import os


class Config(object):
    def __init__(self):
        config_file = os.getenv("CONFIG_FILE", "")
        file_config = dict()
        if config_file:
            with open(config_file) as fp:
                file_config = json.load(fp)

        self.processing_width = file_config.get("processing_width", 1920)
        self.processing_height = file_config.get("processing_height", 1080)
        self.image_debug_mode = file_config.get("image_debug_mode", False)
        self.disable_resize = file_config.get("disable_resize", False)
        self.left_eye_landmarks = file_config.get("left_eye_landmarks", [36, 37, 38, 39, 40, 41])
        self.right_eye_landmarks = file_config.get("right_eye_landmarks", [42, 43, 44, 45, 46, 47])

        self.blur_threshold = file_config.get("blur_threshold", 45)
        self.exposure_threshold_low = file_config.get("exposure_threshold_low", 22)
        self.exposure_threshold_high = file_config.get("exposure_threshold_high", 80)
        # eye ratio -> close eyes 2.8 half close 2.7 full open 1.7 normal open 1.12
        self.open_eye_threshold_low = file_config.get("open_eye_threshold_low", 1.5)
        self.open_eye_threshold_high = file_config.get("open_eye_threshold_high", 3)
        self.face_similarity_tolerance = file_config.get("face_similarity_tolerance", 0.5)


config = Config()
