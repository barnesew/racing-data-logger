from os import path, fsync
import logging
from pathlib import Path

from race_logger.utils import TimeUtils, SettingsUtils
from race_logger.utils.SocketUtils import event_bus
from race_logger.structures.CANData import CANData
from race_logger.structures.GPSData import GPSData
from race_logger.structures.IMUData import IMUData


class Logger:

    def __init__(self):

        self.is_logging = True
        self.last_can_data = CANData()
        self.last_gps_data = GPSData()
        self.last_imu_data = IMUData()

        # Open/Create output log file.
        output_file_name: str = SettingsUtils.get("event_name") + "_" + SettingsUtils.get("session_name") + \
                                "_" + TimeUtils.get_log_name_timestamp() + ".csv"
        output_file_name = output_file_name.lower().replace(" ", "_")
        filename = Path(path.join(
            SettingsUtils.get("dev_settings", "environment_settings", "output_folder"),
            output_file_name
        ))
        filename.touch(exist_ok=True)
        try:
            self.output_file = open(path.join(
                SettingsUtils.get("dev_settings", "environment_settings", "output_folder"),
                output_file_name
            ), "w+")
        except Exception as e:
            logging.error("There was an error while attempting to open the racing log file.")
            logging.error(e)
            return
        try:
            self.output_file.write(GPSData.get_csv_header() + ", " + CANData.get_csv_header() +
                               ", " + IMUData.get_csv_header() + ", Current Lap Distance\n")
        except Exception as e:
            logging.error("There was an error while attempting to write to the racing log file.")
            logging.error(e)
            return

        # Bind handler functions to event bus messages.
        event_bus.on("can_data", self.can_data_handler)
        event_bus.on("imu_data", self.imu_data_handler)
        event_bus.on("gps_data", self.gps_data_handler)
        event_bus.on("lap_distance", self.lap_distance_handler)

    async def can_data_handler(self, can_data: CANData):
        self.last_can_data = can_data

    async def gps_data_handler(self, gps_data: GPSData):
        self.last_gps_data = gps_data

    async def imu_data_handler(self, imu_data: IMUData):
        self.last_imu_data = imu_data

    async def lap_distance_handler(self, lap_distance: float):
        if self.is_logging:
            self.output_file.write(
                self.last_gps_data.get_gps_as_csv() + ", " + self.last_can_data.get_can_as_csv() +
                ", " + self.last_imu_data.get_imu_as_csv() + ", " + str(lap_distance) + "\n"
            )
            self.output_file.flush()
            fsync(self.output_file.fileno())
