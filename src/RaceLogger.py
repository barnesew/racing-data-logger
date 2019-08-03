from threading import Thread
from os import path
from time import sleep

from src.utils import SettingsUtils, TimeUtils
from src.utils import FileUtils
from src.utils import GPSUtils
from src.utils.BusUtils import event_bus
from src.streams.CANStream import CANStream
from src.streams.GPSStream import GPSStream
from src.streams.IMUStream import IMUStream
from src.structures.GPSData import GPSData
from src.Logger import Logger


class RaceLogger (Thread):

    def __init__(self):

        Thread.__init__(self)

        self.logger = Logger()
        self.can_stream = CANStream()
        self.gps_stream = GPSStream()
        self.imu_stream = IMUStream()

        self.track = FileUtils.load_json_from_file(path.join(
            SettingsUtils.get("dev_settings", "environment_settings", "tracks_folder"),
            SettingsUtils.get("current_track_file")
        ))
        self.start_line_first_coordinate = GPSData(
            lat=self.track["start_line"]["first_coordinate"][0],
            lon=self.track["start_line"]["first_coordinate"][1]
        )
        self.start_line_second_coordinate = GPSData(
            lat=self.track["start_line"]["second_coordinate"][0],
            lon=self.track["start_line"]["second_coordinate"][1]
        )

        self.laps_remaining = SettingsUtils.get("race_mode_settings", "laps")
        self.time_remaining = SettingsUtils.get("race_mode_settings", "minutes")

        self.is_triggered = False
        self.time_triggered = None
        self.start_line_crosses = 0
        self.current_lap_gps_points = []
        self.current_lap_distance = 0

        event_bus.on("gps_data")(self._gps_data_handler)

    def run(self) -> None:
        self.can_stream.start()
        self.gps_stream.start()
        self.imu_stream.start()
        while True:
            sleep(5)

    def _gps_data_handler(self, gps_data: GPSData):
        self.current_lap_gps_points.append(gps_data)
        if len(self.current_lap_gps_points) >= 2:
            self.current_lap_distance += GPSUtils.meters_distance_between(
                self.current_lap_gps_points[-2], self.current_lap_gps_points[-1]
            )
            event_bus.emit("lap_distance", self.current_lap_distance)
            was_start_line_crossed, cross_gps = GPSUtils.did_driver_cross_start_line(
                self.current_lap_gps_points[-2], self.current_lap_gps_points[-1],
                self.start_line_first_coordinate, self.start_line_second_coordinate
            )
            if was_start_line_crossed:
                self.start_line_crosses += 1
                self.current_lap_gps_points = [self.current_lap_gps_points[-1]]
                self.current_lap_distance = GPSUtils.meters_distance_between(
                    cross_gps, self.current_lap_gps_points[0]
                )
        if not self.is_triggered:
            self._handle_not_triggered(gps_data)
        else:
            self._handle_triggered(gps_data)

    def _handle_not_triggered(self, gps_data: GPSData):
        if SettingsUtils.get("race_mode_settings", "triggers", "speed") and \
                gps_data.speed > SettingsUtils.get("race_mode_settings", "speed_trigger"):
            self._trigger_start()
        elif SettingsUtils.get("race_mode_settings", "triggers", "one_start_line_pass") and \
                self.start_line_crosses >= 1:
            self._trigger_start()
        elif SettingsUtils.get("race_mode_settings", "triggers", "two_start_line_passes") and \
                self.start_line_crosses >= 2:
            self._trigger_start()

    def _handle_triggered(self, gps_data: GPSData):
        event_bus.emit("laps_remaining", self.laps_remaining - self.start_line_crosses)
        event_bus.emit("time_remaining", SettingsUtils.get("race_mode_settings", "minutes") * 60 -\
                       (TimeUtils.get_precise_timestamp() - self.time_triggered))
        if SettingsUtils.get("race_mode_settings", "countdown_mode") == "laps" and\
                self.laps_remaining - self.start_line_crosses <= 0:
            self._trigger_stop()
            event_bus.emit("laps_remaining", 0)
        elif SettingsUtils.get("race_mode_settings", "countdown_mode") == "minutes" and\
                TimeUtils.get_precise_timestamp() - self.time_triggered >=\
                SettingsUtils.get("race_mode_settings", "minutes") * 60:
            self._trigger_stop()
            event_bus.emit("time_remaining", 0)

    def _trigger_start(self):
        self.start_line_crosses = 0
        self.time_triggered = TimeUtils.get_precise_timestamp()
        self.logger.is_logging = True
        self.is_triggered = True

    def _trigger_stop(self):
        self.logger.is_logging = False
        event_bus.remove_event("_gps_data_handler", "gps_data")
