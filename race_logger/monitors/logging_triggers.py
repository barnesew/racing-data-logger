import asyncio
import logging

from awebus import Bus

from race_logger.utils import SettingsUtils

_race_mode_settings = SettingsUtils.get_setting("race_mode_settings")

_event_bus: Bus = None
_lap_count = 0
_laps_remaining = _race_mode_settings["laps"]


async def logging_triggers(event_bus: Bus):
    global _event_bus
    _event_bus = event_bus
    if _race_mode_settings["triggers"]["one_start_line_pass"] or \
            _race_mode_settings["triggers"]["two_start_line_passes"]:
        event_bus.on("start_line_crossed", _handle_start_line_crossed_pre_trigger)
    if _race_mode_settings["triggers"]["speed"]:
        event_bus.on("gps_data", _handle_gps_data)
    event_bus.on("start_logging", _handle_start_logging)


async def _handle_start_line_crossed_pre_trigger(_timestamp, _gps_coordinate):
    global _lap_count
    _lap_count += 1
    if _lap_count == 1 and _race_mode_settings["triggers"]["one_start_line_pass"] or \
            _lap_count == 2 and _race_mode_settings["triggers"]["two_start_line_passes"]:
        if _lap_count == 1:
            logging.info("One start line pass triggered.")
        else:
            logging.info("Two start line passes triggered.")
        await _event_bus.emitAsync("start_logging")


async def _handle_gps_data(_timestamp, _gps_coordinate, speed, _climb, _heading):
    if speed > _race_mode_settings["speed_trigger"] and _race_mode_settings["triggers"]["speed"]:
        logging.info("Speed triggered.")
        await _event_bus.emitAsync("start_logging")


async def _handle_start_logging():
    if _race_mode_settings["triggers"]["one_start_line_pass"] or \
            _race_mode_settings["triggers"]["two_start_line_passes"]:
        _event_bus.off("start_line_crossed", _handle_start_line_crossed_pre_trigger)
    if _race_mode_settings["triggers"]["speed"]:
        _event_bus.off("gps_data", _handle_gps_data)
    _event_bus.off("start_logging", _handle_start_logging)
    if _race_mode_settings["countdown_mode"] == "laps":
        _event_bus.on("start_line_crossed", _handle_start_line_crossed_post_trigger)
    elif _race_mode_settings["countdown_mode"] == "minutes":
        await asyncio.sleep(_race_mode_settings["minutes"] * 60)
        logging.info("Minutes countdown completed.")
        await _event_bus.emitAsync("stop_logging")


async def _handle_start_line_crossed_post_trigger(_timestamp, _gps_coordinate):
    global _laps_remaining
    _laps_remaining -= 1
    if _lap_count <= 0:
        _event_bus.off("start_line_crossed", _handle_start_line_crossed_post_trigger)
        logging.info("Laps countdown completed.")
        await _event_bus.emitAsync("stop_logging")
