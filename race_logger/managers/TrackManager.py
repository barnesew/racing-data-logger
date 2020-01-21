import logging
from os import listdir, path

from awebus import Bus

from race_logger.structures.GPSData import GPSData
from race_logger.utils import FileUtils, SettingsUtils


_event_bus = None
_tracks: dict = {}
_current_track_name = ""
_current_track = {}


async def init(event_bus):

    global _event_bus, _tracks, _current_track_name, _current_track

    _event_bus = event_bus
    _tracks = _init_load_tracks()

    if _tracks:
        _current_track_name = next(iter(_tracks))
        _current_track = _tracks[_current_track_name]

    await _set_track(SettingsUtils.get("current_track_file"))

    _event_bus.on("set_track", _set_track)
    _event_bus.on("get_current_track", _get_current_track)
    _event_bus.on("get_current_start_line", _get_current_start_line)
    _event_bus.on("list_tracks", _list_tracks)


def _init_load_tracks():

    tracks = {}
    track_directory = SettingsUtils.get("dev_settings", "environment_settings", "tracks_folder")

    if not path.isdir(track_directory):
        logging.error("The track directory specified is not a valid directory.")
        return tracks

    for file in listdir(track_directory):
        if file.endswith(".json"):
            try:
                tracks[path.splitext(file)[0]] = FileUtils.load_json_from_file(path.join(
                    track_directory, file
                ))
            except Exception as e:
                logging.error("There was an error parsing the following track file: " + file)
                logging.error(e)

    return tracks


async def _set_track(track_name):
    global _current_track_name, _current_track
    if track_name in _tracks.keys():
        _current_track_name = track_name
        _current_track = _tracks[track_name]


async def _get_current_track():
    return _current_track


async def _get_current_start_line():
    if _current_track_name == "":
        return [GPSData(), GPSData()]
    return (
        GPSData(
            lat=_current_track["start_line"]["first_coordinate"][0],
            lon=_current_track["start_line"]["first_coordinate"][1]
        ),
        GPSData(
            lat=_current_track["start_line"]["second_coordinate"][0],
            lon=_current_track["start_line"]["second_coordinate"][1]
        )
    )


async def _list_tracks():
    return _tracks.keys()
