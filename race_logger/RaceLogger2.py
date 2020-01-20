import asyncio
from aiohttp import web
import socketio
from awebus import Bus
import logging

from race_logger.utils import LoggingUtils
from race_logger.streams.CANStreamExample import report_can_data
from race_logger.streams.GPSStreamExample import report_gps_data
from race_logger.streams.IMUStreamExample import report_imu_data
from race_logger.publishers.DataPublisher import DataPublisher
from race_logger.managers.RaceManager import RaceManager
from race_logger.managers.LoggingManager import LoggingManager
from race_logger.managers.TrackManager import TrackManager
from race_logger.managers.LapManager import LapManager
from race_logger.managers.TriggerManager import TriggerManager


async def run():

    # LoggingUtils.configure_logging()
    logging.info("Starting RaceLogger.")

    # sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
    # app = web.Application()
    # sio.attach(app)

    event_bus = Bus()

    race_manager = RaceManager(event_bus)
    # logging_manager = LoggingManager(event_bus)

    # _start_web_app(app)

    TrackManager(event_bus)
    LapManager(event_bus)
    TriggerManager(event_bus)
    # DataPublisher(event_bus, sio)

    await asyncio.gather(
        report_can_data(event_bus),
        report_gps_data(event_bus),
        report_imu_data(event_bus)
    )


def _start_web_app(app):
    web.run_app(app, port=5000)
