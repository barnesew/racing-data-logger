from threading import Thread
import time
from random import random

from src.utils.BusUtils import event_bus
from src.structures.CANData import CANData


class CANStream (Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # While loop pushing CAN data
        while True:
            time.sleep(0.04)
            event_bus.emit("can_data", CANData(
                random(), random(), random(), random(), random(), random(), random(), random(), random()
            ))