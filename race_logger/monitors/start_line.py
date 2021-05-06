from awebus import Bus

from geopy.distance import distance

from race_logger.utils import SettingsUtils

_event_bus: Bus = None
_track_id = SettingsUtils.get_setting("current_track")
_start_line_gps_a = SettingsUtils.get_track(_track_id, "start_line", "gps_a")
_start_line_gps_b = SettingsUtils.get_track(_track_id, "start_line", "gps_b")
_current_lap_gps_coordinates = []
_current_lap_timestamps = []
_current_lap_distance = 0


async def start_line(event_bus: Bus):
    global _event_bus
    _event_bus = event_bus
    event_bus.on("gps_data", _handle_gps_data)


async def _handle_gps_data(timestamp, gps_coordinate, _speed, _climb, _heading):
    global _event_bus, _current_lap_gps_coordinates, _current_lap_timestamps, _current_lap_distance
    if not _current_lap_gps_coordinates:
        _current_lap_timestamps.append(timestamp)
        _current_lap_gps_coordinates.append(gps_coordinate)
        return
    did_cross, crossing_gps_coordinate, crossing_timestamp = _did_cross_start_line(
        _current_lap_gps_coordinates[-1], _current_lap_timestamps[-1],
        gps_coordinate, timestamp,
        _start_line_gps_a, _start_line_gps_b
    )
    if did_cross:
        _current_lap_distance += distance(_current_lap_gps_coordinates[-1], crossing_gps_coordinate).meters
        await _event_bus.emitAsync("lap_distance", crossing_timestamp, _current_lap_distance)
        await _event_bus.emitAsync("start_line_crossed", crossing_timestamp, crossing_gps_coordinate)
        _current_lap_gps_coordinates = [crossing_gps_coordinate, gps_coordinate]
        _current_lap_timestamps = [crossing_timestamp, timestamp]
        _current_lap_distance = distance(crossing_gps_coordinate, gps_coordinate).meters
    else:
        _current_lap_timestamps.append(timestamp)
        _current_lap_gps_coordinates.append(gps_coordinate)
        _current_lap_distance += distance(_current_lap_gps_coordinates[-2], _current_lap_gps_coordinates[-1]).meters
    await _event_bus.emitAsync("lap_distance", timestamp, _current_lap_distance)


def _did_cross_start_line(
        driver_gps_a, driver_gps_a_timestamp,
        driver_gps_b, driver_gps_b_timestamp,
        start_line_gps_a, start_line_gps_b
) -> (bool, tuple, float):

    """
    Method to determine if the driver crossed the start line, and if so, determine
    the exact timestamp of when it was crossed.
    Based on an algorithm from "Tricks of the Windows Game Programming Gurus (2nd Edition)"
    """

    if driver_gps_a == driver_gps_b:
        return False, tuple(), 0.0

    gps_s1 = (driver_gps_b[0] - driver_gps_a[0], driver_gps_b[1] - driver_gps_a[1])
    gps_s2 = (start_line_gps_b[0] - start_line_gps_a[0], start_line_gps_b[1] - start_line_gps_a[1])

    s = (-gps_s1[1] * (driver_gps_a[0] - start_line_gps_a[0]) + gps_s1[0] * (driver_gps_a[1] - start_line_gps_a[1])) / \
        (-gps_s2[0] * gps_s1[1] + gps_s1[0] * gps_s2[1])
    t = (gps_s2[0] * (driver_gps_a[1] - start_line_gps_a[1]) - gps_s2[1] * (driver_gps_a[0] - start_line_gps_a[0])) / \
        (-gps_s2[0] * gps_s1[1] + gps_s1[0] * gps_s2[1])

    if not (0 <= s <= 1 and 0 <= t <= 1):
        return False, tuple(), 0.0

    gps_result = [driver_gps_a[0] + (t * gps_s1[0]), driver_gps_a[1] + (t * gps_s1[1])]

    distance_a = distance(driver_gps_a, gps_result).meters
    distance_b = distance(driver_gps_b, gps_result).meters

    gps_result_timestamp = driver_gps_a_timestamp + abs(driver_gps_b_timestamp - driver_gps_a_timestamp) * \
        distance_a / (distance_a + distance_b)

    return True, gps_result, gps_result_timestamp
