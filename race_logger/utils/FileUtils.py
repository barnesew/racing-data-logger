import json
import logging
from os import fsync


def load_json_from_file(file_path):
    logging.debug("Accessing JSON from: " + file_path)
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        logging.error("There was an error trying to load the following JSON file: " + file_path)
        logging.error(e)


def open_file(file_path):
    file = None
    try:
        file = open(file_path, "w+")
    except Exception as e:
        logging.error("There was an error while attempting to create one of the racing log files.")
        logging.error(e)
    return file


def write_to_file(file, line):
    if file is None:
        logging.error("One of the racing log files was not created properly.")
        return
    try:
        file.write(line)
    except Exception as e:
        logging.error("There was an error while writing to one of the racing log files.")
        logging.error(e)
        return
    try:
        file.flush()
        fsync(file.fileno())
    except Exception as e:
        logging.error("There was an error while syncing one of the racing log files with the file system.")
        logging.error(e)
