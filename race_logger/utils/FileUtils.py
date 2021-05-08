import json
import logging
import sys


def load_json_from_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def configure_logging():
    logging.getLogger().setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logging.getLogger().addHandler(stream_handler)
    file_handler = logging.FileHandler(filename="debug.log", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    logging.debug("Logging configured.")
