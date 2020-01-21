import asyncio
from awebus import Bus
import logging

from race_logger.utils import LoggingUtils
from race_logger.streams.CANStreamExample import report_can_data
from race_logger.streams.GPSStreamExample import report_gps_data
from race_logger.streams.IMUStreamExample import report_imu_data
from race_logger.publishers.DataPublisher import DataPublisher
from race_logger.managers import LoggingManager, TrackManager, LapManager, TriggerManager


async def run():

    LoggingUtils.configure_logging()

    logging.info("Welcome to the Racing Data Logger!")

    # TODO: Add the socket.io publisher back in so data is available for the GUI.

    # sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
    # app = web.Application()
    # sio.attach(app)
    # _start_web_app(app)

    event_bus = Bus()

    logging.debug("Starting the race managers.")

    await LoggingManager.init(event_bus)
    await TrackManager.init(event_bus)
    await LapManager.init(event_bus)
    await TriggerManager.init(event_bus)
    # DataPublisher(event_bus, sio)

    logging.debug("Starting the data streams.")

    await asyncio.gather(
        report_can_data(event_bus),
        report_gps_data(event_bus),
        report_imu_data(event_bus)
    )

'''
def _start_web_app(app):
    web.run_app(app, port=5000)
'''
