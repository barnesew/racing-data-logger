from aiohttp import web
import socketio
from awebus import Bus

# from race_logger.Race import Race
# from race_logger.utils import LoggingUtils
from race_logger.streams.CANStreamExample import report_can_data
from race_logger.streams.GPSStreamExample import report_gps_data
from race_logger.streams.IMUStreamExample import report_imu_data

from race_logger.structures.CANData import CANData
from race_logger.structures.GPSData import GPSData
from race_logger.structures.IMUData import IMUData


def start():

    sio = socketio.AsyncServer(async_mode="aiohttp")
    app = web.Application()
    sio.attach(app)

    event_bus = Bus()

    async def handle_can_data(can_data: CANData):
        await sio.emit("can_data", can_data.__dict__)
    event_bus.on("can_data", handle_can_data)

    async def handle_gps_data(gps_data: GPSData):
        await sio.emit("gps_data", gps_data.__dict__)
    event_bus.on("gps_data", handle_gps_data)

    async def handle_imu_data(imu_data: IMUData):
        await sio.emit("imu_data", imu_data.__dict__)
    event_bus.on("imu_data", handle_imu_data)

    # LoggingUtils.configure_logging()
    # logging.info("Starting RaceLogger.")
    # Race()

    sio.start_background_task(report_can_data, event_bus)
    sio.start_background_task(report_gps_data, event_bus)
    sio.start_background_task(report_imu_data, event_bus)

    web.run_app(app, port=5000)
