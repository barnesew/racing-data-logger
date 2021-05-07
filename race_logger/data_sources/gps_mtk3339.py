import logging

import gps
import asyncio
import subprocess

from awebus import Bus

from race_logger.utils import TimeUtils

while subprocess.call(["gpsctl", "-c", "0.2"]):
    logging.warning("gpsctl was unable to update GPS frequency, trying again...")
    continue
_gpsd = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)


async def gps_mtk3339(event_bus: Bus):
    logging.info("Starting GPS MTK3339 data source.")
    loop = asyncio.get_event_loop()
    last_gps_entry = tuple()
    while True:
        gps_raw = await loop.run_in_executor(None, _gpsd.next)
        if gps_raw["class"] != "TPV":
            continue
        coordinate = (
            getattr(gps_raw, "lat", None),
            getattr(gps_raw, "lon", None),
            getattr(gps_raw, "alt", None)
        )
        speed = getattr(gps_raw, "speed", None)
        climb = getattr(gps_raw, "climb", None)
        heading = getattr(gps_raw, "track", None)
        gps_entry = (coordinate, speed, climb, heading)
        if gps_entry == last_gps_entry:
            continue
        last_gps_entry = gps_entry
        # timestamp, gps coordinate, speed, climb, heading
        await event_bus.emitAsync("gps_data", TimeUtils.get_precise_timestamp(), *gps_entry)
