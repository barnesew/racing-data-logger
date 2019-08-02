import queue
import threading
import time

from ..structures.GpsData import GpsData


class GpsWorker (threading.Thread):

    def __init__(self, output_stream: queue.Queue):
        threading.Thread.__init__(self)
        self.output: queue.Queue = output_stream

    def run(self):
        # While loop pushing GPS data
        while True:
            self.output.put(GpsData(lat=39.135464, lon=-84.520143))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.135583, lon=-84.520660))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.136145, lon=-84.521360))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.136525, lon=-84.521763))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.136525, lon=-84.521763))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.138831, lon=-84.523910))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.139547, lon=-84.524361))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.140379, lon=-84.523202))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.140936, lon=-84.520981))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.141094, lon=-84.519683))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.140345, lon=-84.519501))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.139382, lon=-84.519637))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.138308, lon=-84.519755))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.137293, lon=-84.519852))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.136070, lon=-84.519959))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.136525, lon=-84.521763))
            time.sleep(0.9)
            self.output.put(GpsData(lat=39.136525, lon=-84.521763))
            time.sleep(0.9)
