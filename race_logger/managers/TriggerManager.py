import logging

from awebus import Bus

from race_logger.structures.GPSData import GPSData
from race_logger.utils import SettingsUtils


_event_bus = None
_is_triggered = False
_start_line_crosses = 0

_laps_remaining = SettingsUtils.get("race_mode_settings", "laps")
_time_remaining = SettingsUtils.get("race_mode_settings", "minutes")

_trigger_speed = SettingsUtils.get("race_mode_settings", "speed_trigger")
_trigger_on_speed = SettingsUtils.get("race_mode_settings", "triggers", "speed")
_trigger_on_one_pass = SettingsUtils.get("race_mode_settings", "triggers", "one_start_line_pass")
_trigger_on_two_pass = SettingsUtils.get("race_mode_settings", "triggers", "two_start_line_passes")


# TODO: Add stop trigger (Includes laps/time remaining messages).


async def init(event_bus: Bus):

    global _event_bus

    logging.debug("Initializing the trigger manager.")

    _event_bus = event_bus
    _enable_event_callbacks()


async def _lap_handler():
    global _start_line_crosses
    _start_line_crosses += 1
    if _trigger_on_one_pass and _start_line_crosses >= 1:
        logging.debug("The one pass start trigger was tripped.")
        await _trip_trigger()
    elif _trigger_on_two_pass and _start_line_crosses >= 2:
        logging.debug("The two pass start trigger was tripped.")
        await _trip_trigger()


async def _gps_handler(gps_data: GPSData):
    if _trigger_on_speed and gps_data.speed > _trigger_speed:
        logging.debug("The speed start trigger was tripped.")
        await _trip_trigger()


async def _trip_trigger():
    await _event_bus.emitAsync("trigger_tripped")
    _disable_event_callbacks()


async def _reset_trigger():
    _enable_event_callbacks()


def _enable_event_callbacks():
    _event_bus.on("crossed_start_line", _lap_handler)
    _event_bus.on("gps_data", _gps_handler)


def _disable_event_callbacks():
    _event_bus.off("crossed_start_line", _lap_handler)
    _event_bus.off("gps_data", _gps_handler)
