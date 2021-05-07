import asyncio
import logging

from awebus import Bus
from mpu6050 import mpu6050

from race_logger.utils import TimeUtils

_sensor = mpu6050(0x68)


async def imu_mpu6050(event_bus: Bus):
    logging.info("Starting IMU MPU6050 data source.")
    loop = asyncio.get_event_loop()
    while True:
        accel_raw, gyro_raw, _ = await loop.run_in_executor(None, _sensor.get_all_data)
        imu_data = (
            (accel_raw["x"], accel_raw["y"], accel_raw["z"]),
            (gyro_raw["x"], gyro_raw["y"], gyro_raw["z"])
        )
        # timestamp, accelerometer_data, gyro_data
        await event_bus.emitAsync("imu_data", TimeUtils.get_precise_timestamp(), *imu_data)
