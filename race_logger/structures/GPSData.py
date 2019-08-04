from race_logger.utils import TimeUtils


class GPSData:

    """
    lat, lon, alt, speed, climb, heading
    """

    def __init__(self, timestamp: float = None, lat: float = None, lon: float = None, alt: float = None,
                 speed: float = None, climb: float = None, heading: float = None):

        if timestamp is None:
            timestamp = TimeUtils.get_precise_timestamp()

        self.timestamp: float = timestamp
        self.lat: float = lat
        self.lon: float = lon
        self.alt: float = alt
        self.speed: float = speed
        self.climb: float = climb
        self.heading: float = heading

    def get_coordinate_as_tuple(self) -> (float, float):
        return self.lat, self.lon

    @staticmethod
    def get_csv_header():
        return "Timestamp, Latitude, Longitude, Altitude, Speed, Climb, Heading"

    def get_gps_as_csv(self):
        return "{}, {}, {}, {}, {}, {}, {}". format(
            self.timestamp,
            self.lat,
            self.lon,
            self.alt,
            self.speed,
            self.climb,
            self.heading
        )

    def __str__(self):
        return "(" + str(self.lat) + ", " + str(self.lon) + ")"
