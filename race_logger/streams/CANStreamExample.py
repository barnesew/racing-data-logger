import asyncio
from random import random

from race_logger.utils.SocketUtils import event_bus
from race_logger.structures.CANData import CANData


async def report_can_data():
    while True:
        await asyncio.sleep(0.04)
        await event_bus.emitAsync("can_data", CANData(
            random(), random(), random(), random(), random(), random(), random(), random(), random()
        ))
