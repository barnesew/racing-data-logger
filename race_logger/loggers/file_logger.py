import io

from awebus import Bus
import os

from race_logger.utils import SettingsUtils, TimeUtils

_event_bus: Bus = None
_gps_log: io.TextIOWrapper = None
_imu_log: io.TextIOWrapper = None
_lap_log: io.TextIOWrapper = None
_current_lap = 1


async def file_logger(event_bus: Bus):
    global _event_bus, _gps_log, _imu_log, _lap_log
    _event_bus = event_bus
    output_folder = os.path.join(
        SettingsUtils.get_setting("dev_settings", "output_folder"),
        "{}_{}_{}".format(
            SettingsUtils.get_setting("event_name"),
            SettingsUtils.get_setting("session_name"),
            TimeUtils.get_log_name_timestamp()
        )
    )
    os.makedirs(output_folder)
    _gps_log = open(os.path.join(output_folder, "gps.csv"), "w")
    _imu_log = open(os.path.join(output_folder, "imu.csv"), "w")
    _lap_log = open(os.path.join(output_folder, "lap.csv"), "w")
    _gps_log.write("timestamp,latitude,longitude,altitude,speed,climb,heading\n")
    _imu_log.write("timestamp,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z\n")
    _lap_log.write("timestamp,lap_number,lap_distance\n")
    event_bus.on("start_logging", _handle_start_logging)


async def _handle_start_logging():
    _event_bus.off("start_logging", _handle_start_logging)
    _event_bus.on("stop_logging", _handle_stop_logging)
    _event_bus.on("gps_data", _handle_gps_data)
    _event_bus.on("imu_data", _handle_imu_data)
    _event_bus.on("lap_distance", _handle_lap_distance)
    _event_bus.on("start_line_crossed", _handle_start_line_crossed)


async def _handle_stop_logging():
    _event_bus.off("stop_logging", _handle_stop_logging)
    _event_bus.off("gps_data", _handle_gps_data)
    _event_bus.off("imu_data", _handle_imu_data)
    _event_bus.off("lap_distance", _handle_lap_distance)
    _event_bus.off("start_line_crossed", _handle_start_line_crossed)


async def _handle_gps_data(timestamp, gps_coordinate, speed, climb, heading):
    _gps_log.write("{},{},{},{},{},{},{}\n".format(
        timestamp, *gps_coordinate, speed, climb, heading
    ))


async def _handle_imu_data(timestamp, accelerometer_data, gyro_data):
    _imu_log.write("{},{},{},{},{},{},{}\n".format(
        timestamp, *accelerometer_data, *gyro_data
    ))


async def _handle_lap_distance(timestamp, lap_distance):
    _lap_log.write("{},{},{}\n".format(
        timestamp, _current_lap, lap_distance
    ))


async def _handle_start_line_crossed(_timestamp, _gps_coordinate):
    global _current_lap
    _current_lap += 1
