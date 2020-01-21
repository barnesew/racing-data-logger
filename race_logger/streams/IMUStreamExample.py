import asyncio
import logging
from random import random

from race_logger.structures.IMUData import IMUData


async def report_imu_data(event_bus):
    logging.debug("Starting to emit IMU example data.")
    while True:
        await event_bus.emitAsync("imu_data", IMUData(
            accel_x=random(),
            accel_y=random(),
            accel_z=random(),
            gyro_x=random(),
            gyro_y=random(),
            gyro_z=random(),
            roll=random(),
            pitch=random(),
            yaw=random()
        ))
        await asyncio.sleep(0.04)
