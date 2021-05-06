import gps
import asyncio
import subprocess

from awebus import Bus

from race_logger.utils import TimeUtils

# Connect GPS to /dev/ttyS0.
# stty -F /dev/ttyS0 raw 9600 cs8 clocal

# Enable read write access on device.
# sudo chmod o+rw /dev/ttyS0

# Tell GPS to change baud rate.
# echo -ne '$PMTK251,115200*1F\r\n' > /dev/ttyS0

# Connect GPS to /dev/ttyS0 at new baud rate.
# stty -F /dev/ttyS0 raw 115200 cs8 clocal

# Tell GPS to increase telemtry to 10hz.
# echo -ne '$PMTK220,100*2F\r\n' > /dev/ttyS0

# Have GPSD scan at an increased frequency.
# gpsctl -c 0.2

subprocess.call(["stty", "-F", "/dev/ttyS0", "raw", "115200", "cs8", "clocal"])
subprocess.call(["gpsctl", "-c", "0.2"])
_gpsd = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)


async def gps_mtk3339(event_bus: Bus):
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
        speed = getattr(gps_raw, "speed", None),
        climb = getattr(gps_raw, "climb", None)
        heading = getattr(gps_raw, "track", None)
        gps_entry = (coordinate, speed, climb, heading)
        if gps_entry == last_gps_entry:
            continue
        last_gps_entry = gps_entry
        # timestamp, gps coordinate, speed, climb, heading
        await event_bus.emitAsync("gps_data", TimeUtils.get_precise_timestamp(), *gps_entry)
