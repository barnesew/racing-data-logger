import asyncio

from awebus import Bus

from race_logger.data_sources.gps_test_data import gps_test_data
from race_logger.monitors.logging_triggers import logging_triggers
from race_logger.monitors.start_line import start_line
from race_logger.loggers.file_logger import file_logger


def main():
    event_bus = Bus()
    event_loop = asyncio.get_event_loop()
    # Data sources.
    event_loop.create_task(gps_test_data(event_bus))
    # event_loop.create_task(imu_mpu6050(event_bus))
    # Monitors.
    #event_loop.create_task(logging_triggers(event_bus))
    #event_loop.create_task(start_line(event_bus))
    # Loggers.
    #event_loop.create_task(file_logger(event_bus))
    # Run forever.
    event_loop.run_forever()


if __name__ == "__main__":
    main()
