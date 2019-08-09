from time import sleep
from race_logger.RaceLogger import RaceLogger


def main():
    race_logger = RaceLogger()
    race_logger.start()
    while True:
        sleep(5)


if __name__ == "__main__":
    main()
