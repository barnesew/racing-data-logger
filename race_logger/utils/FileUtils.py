import json
import logging


def load_json_from_file(file_path):
    logging.debug("Accessing JSON from: " + file_path)
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        logging.error("There was an error trying to load the following JSON file: " + file_path)
        logging.error(e)
