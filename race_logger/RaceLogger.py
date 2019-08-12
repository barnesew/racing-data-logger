import asyncio
import logging

from race_logger.Race import Race
from race_logger.utils import LoggingUtils
from race_logger.streams.CANStreamExample import report_can_data
from race_logger.streams.GPSStreamExample import report_gps_data
from race_logger.streams.IMUStreamExample import report_imu_data


def start():
    LoggingUtils.configure_logging()
    logging.info("Starting RaceLogger.")
    Race()
    loop = asyncio.get_event_loop()
    loop.create_task(report_can_data())
    loop.create_task(report_gps_data())
    loop.create_task(report_imu_data())
    loop.run_forever()
