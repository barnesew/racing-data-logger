import asyncio
from random import random
import logging

from awebus import Bus

from race_logger.structures.CANData import CANData
from race_logger.utils import TimeUtils


async def report_can_data(event_bus):
    logging.debug("Starting to emit CAN example data.")
    while True:
        await event_bus.emitAsync("can_data", event_bus, CANData(
                timestamp=TimeUtils.get_precise_timestamp(),
                engine_speed=random(),
                throttle_position=random(),
                coolant_temp=random(),
                oil_temp=random(),
                intake_air_temp=random(),
                map_sensor=random(),
                battery_voltage=random(),
                fuel_pressure=random(),
                oil_pressure=random()
            ))
        await asyncio.sleep(0.04)
