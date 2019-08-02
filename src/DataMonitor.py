import queue

from src.streams.CANStream import CanWorker
from src.streams.GPSStream import GpsWorker
from src.streams.RasStream import RasWorker


class DataMonitor:

    def __init__(self, track=None):
        self.track = track
        self.canStream = queue.Queue(maxsize=10)
        self.gpsStream = queue.Queue(maxsize=10)
        self.rasStream = queue.Queue(maxsize=10)
        self.canThread = CanWorker(self.canStream)
        self.gpsThread = GpsWorker(self.gpsStream)
        self.rasThread = RasWorker(self.rasStream)

    def set_track(self, track):
        self.track = track

    def start_monitoring(self):
        # self.canThread.start()
        self.gpsThread.start()
        # self.rasThread.start()
        while True:
            while not self.canStream.empty():
                # Handle can data
                print(self.canStream.get())
            while not self.gpsStream.empty():
                # Handle gps data
                print(self.gpsStream.get())
            while not self.rasStream.empty():
                # Handle on-board data
                print(self.rasStream.get())
