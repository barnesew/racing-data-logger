from src.structures.GPSData import GPSData
from src.utils import GPSUtils


def main():
    test1 = GPSData(lat=39.135360, lon=-84.520031)
    test2 = GPSData(lat=39.128186, lon=-84.511164)
    test3 = GPSData(lat=39.135430, lon=-84.510563)
    test4 = GPSData(lat=39.128620, lon=-84.520655)
    result = GPSUtils.did_driver_cross_start_line(test1, test2, test3, test4)
    print(result[0], result[1].timestamp)


if __name__ == "__main__":
    main()
