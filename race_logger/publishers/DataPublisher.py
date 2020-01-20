from race_logger.structures.CANData import CANData
from race_logger.structures.GPSData import GPSData
from race_logger.structures.IMUData import IMUData


class DataPublisher:

    def __init__(self, event_bus, sio):

        self._event_bus = event_bus
        self._sio = sio

        self._event_bus.on("can_data", self.can_handler)
        self._event_bus.on("gps_data", self.gps_handler)
        self._event_bus.on("imu_data", self.imu_handler)

    async def can_handler(self, can_data: CANData):
        await self._sio.emit("can_data", can_data.__dict__)

    async def gps_handler(self, gps_data: GPSData):
        await self._sio.emit("gps_data", gps_data.__dict__)

    async def imu_handler(self, imu_data: IMUData):
        await self._sio.emit("imu_data", imu_data.__dict__)
