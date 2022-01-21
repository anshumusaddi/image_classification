import os
from utils import process_image

if __name__ == '__main__':
    img_path = os.getenv("TEST_IMAGE")
    image_data = process_image(img_path)
    print(image_data)
