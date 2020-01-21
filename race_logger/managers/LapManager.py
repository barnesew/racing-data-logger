import logging

from race_logger.structures.GPSData import GPSData
from race_logger.utils import GPSUtils


_event_bus = None

_current_lap = 0
_current_lap_gps_points = []
_current_lap_distance = 0


async def init(event_bus):

    global _event_bus

    _event_bus = event_bus
    _event_bus.on("gps_data", _gps_handler)
    _event_bus.on("trigger_tripped", _trigger_handler)
    _event_bus.on("get_current_lap", _get_current_lap)


async def _gps_handler(gps_data: GPSData):

    global _current_lap, _current_lap_distance

    _current_lap_gps_points.append(gps_data)

    if len(_current_lap_gps_points) >= 2:

        _current_lap_distance += GPSUtils.meters_distance_between(
            _current_lap_gps_points[-2], _current_lap_gps_points[-1]
        )

        start_line = (await _event_bus.emitAsync("get_current_start_line"))[0]
        was_start_line_crossed, cross_gps = GPSUtils.did_driver_cross_start_line(
            _current_lap_gps_points[-2], _current_lap_gps_points[-1],
            start_line[0], start_line[1]
        )

        if was_start_line_crossed:
            logging.debug("Registered the vehicle crossing the start line.")
            _current_lap += 1
            await _event_bus.emitAsync("crossed_start_line")
            current_lap_gps_points = [_current_lap_gps_points[-1]]
            _current_lap_distance = GPSUtils.meters_distance_between(
                cross_gps, current_lap_gps_points[0]
            )

    await _event_bus.emitAsync("lap_distance", _current_lap_distance)


async def _trigger_handler():
    global _current_lap
    _current_lap = 0


async def _get_current_lap():
    return _current_lap
