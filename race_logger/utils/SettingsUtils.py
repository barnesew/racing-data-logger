from copy import copy

from race_logger.utils import FileUtils

settings = FileUtils.load_json_from_file("./data/settings.json")


def get(*argv):
    global settings
    temp_settings = copy(settings)
    for setting in argv:
        if setting in temp_settings:
            temp_settings = temp_settings[setting]
        else:
            return None
    return temp_settings
