import asyncio
from threading import Thread

from race_logger.Race import Race
from race_logger.streams.CANStreamExample import report_can_data
from race_logger.streams.GPSStreamExample import report_gps_data
from race_logger.streams.GPSStream import report_gps_data
from race_logger.streams.IMUStreamExample import report_imu_data


class RaceLogger (Thread):

    def __init__(self):

        Thread.__init__(self)
        self.race = Race()

        self.event_loop = asyncio.get_event_loop()
        self.event_loop.create_task(report_can_data())
        self.event_loop.run_in_executor(None, report_gps_data)
        self.event_loop.create_task(report_imu_data())

    def run(self) -> None:
        self.event_loop.run_forever()
