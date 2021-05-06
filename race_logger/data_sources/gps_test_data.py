import asyncio

from awebus import Bus

from race_logger.utils import TimeUtils

_test_data = (
    [(39.135323, -84.519985, 0), 20, 0, 45],
    [(39.135407, -84.510656, 0), 21, 1, 135],
    [(39.128031, -84.511234, 0), 22, -2, 225],
    [(39.128627, -84.520753, 0), 23, 1, 315]
)


async def gps_test_data(event_bus: Bus):
    while True:
        for gps_data in _test_data:
            # timestamp, gps coordinate, speed, climb, heading
            await event_bus.emitAsync("gps_data", *tuple([TimeUtils.get_precise_timestamp()] + gps_data))
            await asyncio.sleep(1)
