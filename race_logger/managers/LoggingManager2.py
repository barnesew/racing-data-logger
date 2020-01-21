from os import path, makedirs
import logging

from race_logger.utils import TimeUtils, SettingsUtils, FileUtils
from race_logger.structures.CANData import CANData
from race_logger.structures.GPSData import GPSData
from race_logger.structures.IMUData import IMUData


class LoggingManager:

    def __init__(self, event_bus):

        self.is_logging = True
        self._event_bus = event_bus

        self._output_folder = path.join(
                SettingsUtils.get("dev_settings", "environment_settings", "output_folder"),
                SettingsUtils.get("event_name") + "_" + SettingsUtils.get("session_name") +
                "_" + TimeUtils.get_log_name_timestamp()
            )
        self._output_folder = self._output_folder.lower().replace(" ", "_")

        self._can_file = None
        self._gps_file = None
        self._imu_file = None
        self._distance_file = None

        self._open_files()

        self._event_bus.on("can_data", LoggingManager._can_handler)
        self._event_bus.on("gps_data", LoggingManager._gps_handler)
        self._event_bus.on("imu_data", LoggingManager._imu_handler)
        # self._event_bus.on("lap_distance", self._lap_distance_handler)

    async def _can_handler(self, can_data: CANData):
        FileUtils.write_to_file(self._can_file, can_data.get_can_as_csv())

    async def _gps_handler(self, gps_data: GPSData):
        FileUtils.write_to_file(self._can_file, gps_data.get_gps_as_csv())

    async def _imu_handler(self, imu_data: IMUData):
        FileUtils.write_to_file(self._can_file, imu_data.get_imu_as_csv())

    '''
    async def _lap_distance_handler(self, lap_distance: float):
        if self.is_logging:
            logging.debug("Writing data entry to the racing log file.")
            await asyncio.get_event_loop().run_in_executor(
                None, self.write_to_file,
                self.last_gps_data.get_gps_as_csv() + ", " + self.last_can_data.get_can_as_csv() +
                ", " + self.last_imu_data.get_imu_as_csv() + ", " + str(lap_distance) + "\n"
            )
    '''

    def _open_files(self):

        logging.debug("Creating a directory for the racing log files: " + self._output_folder)
        makedirs(self._output_folder)

        logging.debug("Creating the racing log files.")
        self._can_file = FileUtils.open_file(path.join(self._output_folder, "can_data.csv"))
        self._gps_file = FileUtils.open_file(path.join(self._output_folder, "gps_data.csv"))
        self._imu_file = FileUtils.open_file(path.join(self._output_folder, "imu_data.csv"))
        self._distance_file = FileUtils.open_file(path.join(self._output_folder, "distance_data.csv"))

        logging.debug("Writing CSV headers to the racing log files.")
        FileUtils.write_to_file(self._can_file, CANData.get_csv_header() + "\n")
        FileUtils.write_to_file(self._gps_file, GPSData.get_csv_header() + "\n")
        FileUtils.write_to_file(self._imu_file, IMUData.get_csv_header() + "\n")
        FileUtils.write_to_file(self._distance_file, "Timestamp, Lap Distance\n")
