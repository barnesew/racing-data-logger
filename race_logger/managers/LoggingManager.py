from os import path, fsync
import logging
import asyncio

from race_logger.utils import TimeUtils, SettingsUtils
from race_logger.structures.CANData import CANData
from race_logger.structures.GPSData import GPSData
from race_logger.structures.IMUData import IMUData


class LoggingManager:

    def __init__(self, event_bus):

        self.is_logging = True
        self.last_can_data = CANData()
        self.last_gps_data = GPSData()
        self.last_imu_data = IMUData()

        logging.debug("Opening and writing headers to the racing log file.")
        output_file_name: str = SettingsUtils.get("event_name") + "_" + SettingsUtils.get("session_name") + \
                                "_" + TimeUtils.get_log_name_timestamp() + ".csv"
        output_file_name = output_file_name.lower().replace(" ", "_")
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

        logging.debug("Binding CAN, IMU, GPS, and lap distance handlers to the event bus.")
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
            logging.debug("Writing data entry to the racing log file.")
            await asyncio.get_event_loop().run_in_executor(
                None, self.write_to_file,
                self.last_gps_data.get_gps_as_csv() + ", " + self.last_can_data.get_can_as_csv() +
                ", " + self.last_imu_data.get_imu_as_csv() + ", " + str(lap_distance) + "\n"
            )

    def write_to_file(self, line):
        try:
            self.output_file.write(line)
        except Exception as e:
            logging.error("There was an error while attempting to write to the racing log file.")
            logging.error(e)
            return
        try:
            self.output_file.flush()
            fsync(self.output_file.fileno())
        except Exception as e:
            logging.error("There was an error while attempting to sync file with the file system.")
            logging.error(e)
            return
