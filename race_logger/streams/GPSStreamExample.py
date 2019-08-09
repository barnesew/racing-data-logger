import asyncio

from race_logger.utils.SocketUtils import event_bus
from race_logger.structures.GPSData import GPSData


async def report_gps_data():
    while True:
        await event_bus.emitAsync("gps_data", GPSData(lat=39.135338, lon=-84.520020))
        await asyncio.sleep(0.9)
        await event_bus.emitAsync("gps_data", GPSData(lat=39.135366, lon=-84.510619))
        await asyncio.sleep(0.9)
        await event_bus.emitAsync("gps_data", GPSData(lat=39.128228, lon=-84.511034))
        await asyncio.sleep(0.9)
        await event_bus.emitAsync("gps_data", GPSData(lat=39.128633, lon=-84.520651))
        await asyncio.sleep(0.9)
