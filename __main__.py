import argparse
import concurrent.futures
import datetime
import json
import os

from config import config
from utils import process_image, process_directory, imread, load_known_images
from utils.process_score import process_score


def process_image_and_update(image, known_faces, actual_data):
    image_data = process_image(image, known_faces)
    actual_data.update(image_data)


def __main__(img_directory, face_img_directory=None):
    if face_img_directory:
        known_faces = load_known_images(face_img_directory)
    else:
        known_faces = None
    images_clustered = process_directory(img_directory)
    directory_data = list()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=config.thread_count)
    futures = list()
    for cluster in images_clustered:
        cluster_data = dict()
        for img_path in cluster:
            dir_img_path = os.path.join(img_directory, img_path)
            image = imread(dir_img_path)
            cluster_data[img_path] = dict()
            futures.append(executor.submit(process_image_and_update, image, known_faces, cluster_data[img_path]))
        directory_data.append(cluster_data)
    concurrent.futures.wait(futures)
    process_score(directory_data)
    return directory_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="An Utility to Auto Select Images From a Directory")
    parser.add_argument("-i", "--image-directory", help="The Image Directory Where Images Are Located")
    parser.add_argument("-f", "--face-directory", help="The Image Directory Where Known Faces Are Located")
    parser.add_argument("-o", "--output-file", help="The File Name To Dump JSON Data")
    args = parser.parse_args()
    image_directory = args.image_directory
    face_directory = args.face_directory
    output_file = args.output_file
    if not image_directory:
        parser.error("No image directory passed. Please specify it using --image-directory")
    start_time = datetime.datetime.now()
    dir_img_data = __main__(image_directory, face_directory)
    if output_file:
        with open(output_file, "w") as fp:
            json.dump(dir_img_data, fp, indent=2)
    else:
        print(json.dumps(dir_img_data, indent=2))
    end_time = datetime.datetime.now()
    print(end_time - start_time)
