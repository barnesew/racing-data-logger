import logging

from race_logger.structures.GPSData import GPSData
from race_logger.utils import GPSUtils


class LapManager:

    def __init__(self, event_bus):

        self._event_bus = event_bus

        self._current_lap = 0
        self._current_lap_gps_points = []
        self._current_lap_distance = 0

        self._event_bus.on("gps_data", self._gps_handler)
        self._event_bus.on("trigger_tripped", self._trigger_handler)
        self._event_bus.on("get_current_lap", self._get_current_lap)

    async def _gps_handler(self, gps_data: GPSData):

        self.current_lap_gps_points.append(gps_data)

        if len(self.current_lap_gps_points) >= 2:

            self.current_lap_distance += GPSUtils.meters_distance_between(
                self.current_lap_gps_points[-2], self.current_lap_gps_points[-1]
            )

            start_line = await self._event_bus.emitAsync("get_current_start_line")[0]
            was_start_line_crossed, cross_gps = GPSUtils.did_driver_cross_start_line(
                self.current_lap_gps_points[-2], self.current_lap_gps_points[-1],
                start_line[0], start_line[1]
            )

            if was_start_line_crossed:
                logging.debug("Registered the vehicle crossing the start line.")
                self._current_lap += 1
                await self._event_bus.emitAsync("crossed_start_line")
                self.current_lap_gps_points = [self.current_lap_gps_points[-1]]
                self.current_lap_distance = GPSUtils.meters_distance_between(
                    cross_gps, self.current_lap_gps_points[0]
                )

        await self._event_bus.emitAsync("lap_distance", self.current_lap_distance)

    async def _trigger_handler(self):
        self._current_lap = 0

    async def _get_current_lap(self):
        return self._current_lap
