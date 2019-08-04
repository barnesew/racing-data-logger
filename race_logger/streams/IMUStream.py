from threading import Thread
import time
from random import random

from race_logger.utils.BusUtils import event_bus
from race_logger.structures.IMUData import IMUData


class IMUStream (Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # While loop pushing on-board data
        while True:
            time.sleep(0.04)
            event_bus.emit("imu_data", IMUData(
                random(), random(), random(), random(), random(), random(), random(), random(), random()
            ))
