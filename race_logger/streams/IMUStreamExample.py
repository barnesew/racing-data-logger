import asyncio
from random import random

from race_logger.utils.SocketUtils import event_bus
from race_logger.structures.IMUData import IMUData


async def report_imu_data():
    while True:
        await asyncio.sleep(0.04)
        await event_bus.emitAsync("imu_data", IMUData(
            random(), random(), random(), random(), random(), random(), random(), random(), random()
        ))
