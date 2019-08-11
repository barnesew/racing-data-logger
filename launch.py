from race_logger import RaceLogger
from race_logger.utils import LoggingUtils


def main():
    LoggingUtils.configure_logging()
    RaceLogger.start()


if __name__ == "__main__":
    main()
