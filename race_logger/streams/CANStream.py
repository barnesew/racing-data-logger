import asyncio
from random import random

from race_logger.utils.SocketUtils import event_bus
from race_logger.structures.CANData import CANData

import RPi.GPIO as GPIO
import can

_led = 22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(_led, GPIO.OUT)
GPIO.output(_led, True)

# For a list of PIDs visit https://en.wikipedia.org/wiki/OBD-II_PIDs
ENGINE_RPM = 0x0C  # RPM
THROTTLE_POSITION = 0x11  # Percentage
ENGINE_COOLANT_TEMP = 0x05  # Degrees Celsius
OIL_TEMP = 0x5C  # Degrees Celsius

PID_REQUEST = 0x7DF
PID_REPLY = 0x7E8


async def report_can_data():
    while True:
        await asyncio.sleep(0.04)
        await sio.emit("can_data", "CAN DATA")
        """
        event_bus.emitAsync("can_data", CANData(
            random(), random(), random(), random(), random(), random(), random(), random(), random()
        ))
        """
