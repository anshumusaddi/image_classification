import argparse
import json
import os
from utils import process_image, process_directory, imread, load_known_images


def __main__(img_directory, face_img_directory=None):
    if face_img_directory:
        known_faces = load_known_images(face_img_directory)
    else:
        known_faces = None
    images_clustered = process_directory(img_directory)
    #print(images_clustered)
    directory_data = list()
    for cluster in images_clustered:
        cluster_data = dict()
        #print(cluster)
        for img_path in cluster:
            #print(img_path)
            dir_img_path = os.path.join(img_directory, img_path)
            image = imread(dir_img_path)
            image_data = process_image(image, known_faces)
            cluster_data[img_path] = image_data
        directory_data.append(cluster_data)
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
    dir_img_data = __main__(image_directory, face_directory)
    if output_file:
        with open(output_file, "w") as fp:
            json.dump(dir_img_data, fp, indent=2)
    else:
        print(json.dumps(dir_img_data, indent=2))
        #print(dir_img_data)
