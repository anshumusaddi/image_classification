import os

from utils import process_image, imread, load_known_images

if __name__ == '__main__':
    img_path = os.getenv("TEST_IMAGE")
    known_face_dir = os.getenv("KNOWN_DIR")
    known_faces = load_known_images(known_face_dir)
    image = imread(img_path)
    image_data = process_image(image, known_faces)
    print(image_data)
