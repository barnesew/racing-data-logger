from ..utils import TimeUtils


class GpsData:

    def __init__(self, timestamp=None, lat=None, lon=None, alt=None, speed=None, climb=None, satellites=None):
        if timestamp is None:
            timestamp = TimeUtils.get_precise_timestamp()
        self.timestamp = timestamp
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.speed = speed
        self.climb = climb
        self.satellites = satellites

    def set_timestamp(self):
        self.timestamp = TimeUtils.get_precise_timestamp()

    def set_coordinate(self, lat, lon, alt):
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def set_speed(self, speed, climb):
        self.speed = speed
        self.climb = climb

    def set_satellites(self, satellites):
        self.satellites = satellites

    def __str__(self):
        return "(" + str(self.lat) + ", " + str(self.lon) + ")"
