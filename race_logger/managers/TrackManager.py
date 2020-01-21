import logging
from os import listdir, path

from awebus import Bus

from race_logger.structures.GPSData import GPSData
from race_logger.utils import FileUtils, SettingsUtils


class TrackManager:

    def __init__(self, event_bus):

        self._event_bus: Bus = event_bus
        self._tracks: dict = self._init_load_tracks()
        self._current_track_name = ""
        self._current_track = {}

        if self._tracks:
            self._current_track_name = next(iter(self._tracks))
            self._current_track = self._tracks[self._current_track_name]

        self._event_bus.on("set_track", self._set_track)
        self._event_bus.on("get_current_track", self._get_current_track)
        self._event_bus.on("get_current_start_line", self._get_current_start_line)
        self._event_bus.on("list_tracks", self._list_tracks)

    @staticmethod
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

    async def _set_track(self, track_name):
        if track_name in self._tracks.keys():
            self._current_track_name = track_name
            self._current_track = self._tracks[track_name]

    async def _get_current_track(self):
        return self._current_track

    async def _get_current_start_line(self):
        if self._current_track_name == "":
            return [GPSData(), GPSData()]
        return (
            GPSData(
                lat=self._current_track["start_line"]["first_coordinate"][0],
                lon=self._current_track["start_line"]["first_coordinate"][1]
            ),
            GPSData(
                lat=self._current_track["start_line"]["second_coordinate"][0],
                lon=self._current_track["start_line"]["second_coordinate"][1]
            )
        )

    async def _list_tracks(self):
        return self._tracks.keys()
