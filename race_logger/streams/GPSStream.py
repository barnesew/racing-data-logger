import gps

from race_logger.utils.SocketUtils import event_bus
from race_logger.structures.GPSData import GPSData

_gpsd = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)


async def report_gps_data():
    while True:
        gps_raw = _gpsd.next()
        if gps_raw["class"] == "TPV":
            gps_data = GPSData(
                lat=getattr(gps_raw, "lat", None),
                lon=getattr(gps_raw, "lon", None),
                alt=getattr(gps_raw, "alt", None),
                speed=getattr(gps_raw, "speed", None),
                climb=getattr(gps_raw, "climb", None),
                heading=getattr(gps_raw, "track", None)
            )
            await event_bus.emitAsync("gps_data", gps_data.__dict__)
