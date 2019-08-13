import asyncio
import logging
from random import random

from race_logger.structures.IMUData import IMUData


async def report_imu_data(event_bus):
    logging.debug("Starting to emit IMU example data.")
    while True:
        await event_bus.emitAsync("imu_data", IMUData(
            random(), random(), random(), random(), random(), random(), random(), random(), random()
        ))
        await asyncio.sleep(0.04)
