import asyncio

from race_logger import RaceLogger2


def main():
    asyncio.run(RaceLogger2.run())


if __name__ == "__main__":
    main()
