from copy import copy

from race_logger.utils import FileUtils

_settings = FileUtils.load_json_from_file("./settings.json")
_tracks = FileUtils.load_json_from_file("./tracks.json")


def get_setting(*argv):
    global _settings
    temp_settings = copy(_settings)
    for setting in argv:
        if setting in temp_settings:
            temp_settings = temp_settings[setting]
        else:
            return None
    return temp_settings


def get_track(*argv):
    global _tracks
    temp_tracks = copy(_tracks)
    for track in argv:
        if track in temp_tracks:
            temp_tracks = temp_tracks[track]
        else:
            return None
    return temp_tracks
