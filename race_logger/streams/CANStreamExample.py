import asyncio
from random import random
import logging

from race_logger.structures.CANData import CANData


async def report_can_data(event_bus):
    logging.debug("Starting to emit CAN example data.")
    while True:
        await event_bus.emitAsync("can_data", CANData(
            random(), random(), random(), random(), random(), random(), random(), random(), random()
        ))
        await asyncio.sleep(0.04)
