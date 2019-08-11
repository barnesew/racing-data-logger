import gps
import asyncio

from race_logger.utils.SocketUtils import event_bus
from race_logger.structures.GPSData import GPSData

_gpsd = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)


async def report_gps_data():
    last_gps = GPSData(lat=0, lon=0)
    while True:
        loop = asyncio.get_event_loop()
        gps_raw = await loop.run_in_executor(None, _gpsd.next)
        if gps_raw["class"] == "TPV":
            gps_data = GPSData(
                lat=getattr(gps_raw, "lat", None),
                lon=getattr(gps_raw, "lon", None),
                alt=getattr(gps_raw, "alt", None),
                speed=getattr(gps_raw, "speed", None),
                climb=getattr(gps_raw, "climb", None),
                heading=getattr(gps_raw, "track", None)
            )
            if last_gps.lat == gps_data.lat and last_gps.lon == gps_data.lon:
                await asyncio.sleep(0.04)
                continue
            await event_bus.emitAsync("gps_data", gps_data)
