from threading import Thread
from os import path
from time import sleep

from src.utils import SettingsUtils
from src.utils import FileUtils
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
        self.is_triggered = False
        self.current_lap_gps_points = []
        event_bus.on("gps_data")(self.gps_data_handler)

    def run(self) -> None:
        self.can_stream.start()
        self.gps_stream.start()
        self.imu_stream.start()
        while True:
            sleep(5)

    def gps_data_handler(self, gps_data: GPSData):
        self.current_lap_gps_points.append(gps_data)
