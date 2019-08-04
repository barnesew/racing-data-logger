from threading import Thread
import time

from race_logger.utils.BusUtils import event_bus
from race_logger.structures.GPSData import GPSData


class GPSStream (Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # While loop pushing GPS data
        while True:
            event_bus.emit("gps_data", GPSData(lat=39.135338, lon=-84.520020))
            time.sleep(0.9)
            event_bus.emit("gps_data", GPSData(lat=39.135366, lon=-84.510619))
            time.sleep(0.9)
            event_bus.emit("gps_data", GPSData(lat=39.128228, lon=-84.511034))
            time.sleep(0.9)
            event_bus.emit("gps_data", GPSData(lat=39.128633, lon=-84.520651))
            time.sleep(0.9)
