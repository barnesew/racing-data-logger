from awebus import Bus

from race_logger.structures.GPSData import GPSData
from race_logger.utils import SettingsUtils


class TriggerManager:

    def __init__(self, event_bus: Bus):

        self._event_bus = event_bus
        self._is_triggered = False
        self._start_line_crosses = 0

        self._laps_remaining = SettingsUtils.get("race_mode_settings", "laps")
        self._time_remaining = SettingsUtils.get("race_mode_settings", "minutes")

        self._trigger_speed = SettingsUtils.get("race_mode_settings", "speed_trigger")
        self._trigger_on_speed = SettingsUtils.get("race_mode_settings", "triggers", "speed")
        self._trigger_on_one_pass = SettingsUtils.get("race_mode_settings", "triggers", "one_start_line_pass")
        self._trigger_on_two_pass = SettingsUtils.get("race_mode_settings", "triggers", "two_start_line_passes")

        self._enable_event_callbacks()

    async def _lap_handler(self):
        self._start_line_crosses += 1
        if self._trigger_on_one_pass and self._start_line_crosses >= 1:
            await self._trip_trigger()
        elif self._trigger_on_two_pass and self._start_line_crosses >= 2:
            await self._trip_trigger()

    async def _gps_handler(self, gps_data: GPSData):
        if self._trigger_on_speed and gps_data.speed > self._trigger_speed:
            await self._trip_trigger()

    async def _trip_trigger(self):
        await self._event_bus.emitAsync("trigger_tripped")
        self._disable_event_callbacks()

    async def _reset_trigger(self):
        self._enable_event_callbacks()

    def _enable_event_callbacks(self):
        self._event_bus.on("crossed_start_line", self._lap_handler)
        self._event_bus.on("gps_data", self._gps_handler)

    def _disable_event_callbacks(self):
        self._event_bus.off("crossed_start_line", self._lap_handler)
        self._event_bus.off("gps_data", self._gps_handler)
