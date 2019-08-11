from copy import copy
import logging

from race_logger.utils import FileUtils

settings = FileUtils.load_json_from_file("./data/settings.json")


def get(*argv):
    global settings
    temp_settings = copy(settings)
    for setting in argv:
        if setting in temp_settings:
            temp_settings = temp_settings[setting]
        else:
            logging.error("One of the required settings was not found. Check the format of settings.json.")
            return None
    return temp_settings
