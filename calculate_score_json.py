import json

from utils.process_score import process_score

if __name__ == '__main__':
    with open("input.json") as fp:
        dir_data = json.load(fp)
    process_score(dir_data)
    with open("output.json", "w") as fp:
        json.dump(dir_data, fp)
