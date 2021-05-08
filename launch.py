import asyncio
import logging

from awebus import Bus

from race_logger.data_sources.gps_mtk3339 import gps_mtk3339
from race_logger.data_sources.imu_mpu6050 import imu_mpu6050
from race_logger.monitors.kalman_filter import kalman_filter
from race_logger.monitors.logging_triggers import logging_triggers
from race_logger.monitors.start_line import start_line
from race_logger.loggers.file_logger import file_logger
from race_logger.utils import FileUtils


def main():

    # Setup logging.
    FileUtils.configure_logging()

    # Setup event loop.
    event_bus = Bus()
    event_loop = asyncio.get_event_loop()

    # Data sources.
    event_loop.create_task(gps_mtk3339(event_bus))
    event_loop.create_task(imu_mpu6050(event_bus))

    # Monitors.
    event_loop.create_task(kalman_filter(event_bus))
    event_loop.create_task(logging_triggers(event_bus))
    event_loop.create_task(start_line(event_bus))

    # Loggers.
    event_loop.create_task(file_logger(event_bus))

    # Start racing data logger.
    logging.info("Starting the Racing Data Logger.")
    event_loop.create_task(event_bus.emitAsync("start_logging"))
    event_loop.run_forever()


if __name__ == "__main__":
    main()
