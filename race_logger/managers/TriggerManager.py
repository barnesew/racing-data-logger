import logging

from awebus import Bus

from race_logger.structures.GPSData import GPSData
from race_logger.utils import SettingsUtils


_event_bus: Bus = None
_is_triggered = False

_laps_remaining = SettingsUtils.get("race_mode_settings", "laps")
_time_remaining = SettingsUtils.get("race_mode_settings", "minutes")

_trigger_speed = SettingsUtils.get("race_mode_settings", "speed_trigger")
_trigger_on_speed = SettingsUtils.get("race_mode_settings", "triggers", "speed")
_trigger_on_one_pass = SettingsUtils.get("race_mode_settings", "triggers", "one_start_line_pass")
_trigger_on_two_pass = SettingsUtils.get("race_mode_settings", "triggers", "two_start_line_passes")


# TODO: Add stop trigger for time. Use setting for stop type.


async def init(event_bus: Bus):

    global _event_bus

    logging.debug("Initializing the trigger manager.")

    _event_bus = event_bus
    _event_bus.on("crossed_start_line", _trigger_set_lap_handler)
    _event_bus.on("gps_data", _trigger_set_gps_handler)


async def _trigger_set_lap_handler():
    current_lap = (await _event_bus.emitAsync("get_current_lap"))[0]
    if _trigger_on_one_pass and current_lap >= 1:
        logging.debug("The one pass start trigger was tripped.")
        await _trip_trigger()
    elif _trigger_on_two_pass and current_lap >= 2:
        logging.debug("The two pass start trigger was tripped.")
        await _trip_trigger()


async def _trigger_set_gps_handler(gps_data: GPSData):
    if _trigger_on_speed and gps_data.speed > _trigger_speed:
        logging.debug("The speed start trigger was tripped.")
        await _trip_trigger()


async def _trigger_tripped_lap_handler():
    current_lap = (await _event_bus.emitAsync("get_current_lap"))[0]
    logging.debug("Laps remaining: {}".format(_laps_remaining - current_lap))
    await _event_bus.emitAsync("laps_remaining", _laps_remaining - current_lap)
    if current_lap >= _laps_remaining:
        logging.debug("The laps remaining stop trigger was tripped.")
        await _reset_trigger()


async def _trip_trigger():
    global _is_triggered
    logging.debug("Trigger has been tripped.")
    _is_triggered = True
    _event_bus.off("crossed_start_line", _trigger_set_lap_handler)
    _event_bus.off("gps_data", _trigger_set_gps_handler)
    _event_bus.on("crossed_start_line", _trigger_tripped_lap_handler)
    await _event_bus.emitAsync("trigger_tripped")


async def _reset_trigger():
    global _is_triggered
    logging.debug("Trigger has been reset.")
    _is_triggered = False
    _event_bus.off("crossed_start_line", _trigger_tripped_lap_handler)
    # _event_bus.on("crossed_start_line", _trigger_set_lap_handler)
    # _event_bus.on("gps_data", _trigger_set_gps_handler)
    await _event_bus.emitAsync("trigger_reset")
