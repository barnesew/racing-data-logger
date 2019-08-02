from threading import Thread

from src.utils import SettingsUtils
from src.utils import FileUtils
from src.streams.CANStream import CANStream
from src.streams.GPSStream import GPSStream
from src.streams.IMUStream import IMUStream


class RaceLogger (Thread):

    def __init__(self):
        Thread.__init__(self)
        self.canThread = CANStream()
        self.gpsThread = GPSStream()
        self.imuThread = IMUStream()
        self.track = FileUtils.load_json_from_file(
            SettingsUtils.get('dev_settings', 'environment_settings', 'tracks_folder') +
            SettingsUtils.get('current_track_file')
        )

    def set_track(self, track):
        self.track = track

    def run(self) -> None:
        self.canThread.start()
        self.gpsThread.start()
        self.imuThread.start()
        while True:
            pass
