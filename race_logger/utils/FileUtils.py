import json


def load_json_from_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
