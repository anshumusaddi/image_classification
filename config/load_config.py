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


config = Config()
