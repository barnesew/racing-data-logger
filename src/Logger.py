from src.utils.BusUtils import event_bus
from src.structures.CANData import CANData
from src.structures.IMUData import IMUData
from src.structures.GPSData import GPSData


class Logger:

    def __init__(self):
        self.is_logging = False
        self.last_can_data = CANData()
        self.last_imu_data = IMUData()
        event_bus.on("can_data")(self.can_data_handler)
        event_bus.on("imu_data")(self.imu_data_handler)
        event_bus.on("gps_data")(self.gps_data_handler)

    def can_data_handler(self, can_data: CANData):
        self.last_can_data = can_data

    def imu_data_handler(self, imu_data: IMUData):
        self.last_imu_data = imu_data

    def gps_data_handler(self, gps_data: GPSData):
        if self.is_logging:
            print("Log: ", gps_data.timestamp, ", ", self.last_can_data, ", ", self.last_imu_data)
