from os import path, makedirs
import logging

from race_logger.utils import TimeUtils, SettingsUtils, FileUtils
from race_logger.structures.CANData import CANData
from race_logger.structures.GPSData import GPSData
from race_logger.structures.IMUData import IMUData


_event_bus = None

_output_folder = path.join(
        SettingsUtils.get("dev_settings", "environment_settings", "output_folder"),
        SettingsUtils.get("event_name") + "_" + SettingsUtils.get("session_name") +
        "_" + TimeUtils.get_log_name_timestamp()
    )
_output_folder = _output_folder.lower().replace(" ", "_")

_can_file = None
_gps_file = None
_imu_file = None
_distance_file = None


def init(event_bus):
    global _event_bus
    _event_bus = event_bus
    _open_files()
    _event_bus.on("can_data", _can_handler)
    _event_bus.on("gps_data", _gps_handler)
    _event_bus.on("imu_data", _imu_handler)
    _event_bus.on("lap_distance", _lap_distance_handler)


async def _can_handler(can_data: CANData):
    FileUtils.write_to_file(_can_file, can_data.get_can_as_csv() + "\n")


async def _gps_handler(gps_data: GPSData):
    FileUtils.write_to_file(_gps_file, gps_data.get_gps_as_csv() + "\n")


async def _imu_handler(imu_data: IMUData):
    FileUtils.write_to_file(_imu_file, imu_data.get_imu_as_csv() + "\n")


async def _lap_distance_handler(lap_distance: float):
    FileUtils.write_to_file(_distance_file, "{}, {}\n".format(TimeUtils.get_precise_timestamp(), lap_distance))


def _open_files():

    global _can_file, _gps_file, _imu_file, _distance_file

    logging.debug("Creating a directory for the racing log files: " + _output_folder)
    makedirs(_output_folder)

    logging.debug("Creating the racing log files.")
    _can_file = FileUtils.open_file(path.join(_output_folder, "can_data.csv"))
    _gps_file = FileUtils.open_file(path.join(_output_folder, "gps_data.csv"))
    _imu_file = FileUtils.open_file(path.join(_output_folder, "imu_data.csv"))
    _distance_file = FileUtils.open_file(path.join(_output_folder, "distance_data.csv"))

    logging.debug("Writing CSV headers to the racing log files.")
    FileUtils.write_to_file(_can_file, CANData.get_csv_header() + "\n")
    FileUtils.write_to_file(_gps_file, GPSData.get_csv_header() + "\n")
    FileUtils.write_to_file(_imu_file, IMUData.get_csv_header() + "\n")
    FileUtils.write_to_file(_distance_file, "Timestamp, Lap Distance\n")
