from geopy.distance import distance

from src.structures.GPSData import GPSData


def did_driver_cross_start_line(driver_gps_a: GPSData, driver_gps_b: GPSData,
                                start_line_a: GPSData, start_line_b: GPSData) -> (bool, GPSData):

    """
    Method to determine if the driver crossed the start line, and if so, determine
    the exact timestamp of when it was crossed.
    Based on an algorithm from "Tricks of the Windows Game Programming Gurus (2nd Edition)"

    :param driver_gps_a: Previous GPS point of the driver.
    :param driver_gps_b: Most recent GPS point of the driver.
    :param start_line_a: First start line GPS point.
    :param start_line_b: Second start line GPS point.
    :return: (bool, GPSData) - A boolean for if there was an intersection and a GPSData object
    filled if there was an intersection.
    """

    gps_s1 = GPSData(lat=driver_gps_b.lat - driver_gps_a.lat, lon=driver_gps_b.lon - driver_gps_a.lon)
    gps_s2 = GPSData(lat=start_line_b.lat - start_line_a.lat, lon=start_line_b.lon - start_line_a.lon)

    s = (-gps_s1.lon * (driver_gps_a.lat - start_line_a.lat) + gps_s1.lat * (driver_gps_a.lon - start_line_a.lon)) / \
        (-gps_s2.lat * gps_s1.lon + gps_s1.lat * gps_s2.lon)
    t = (gps_s2.lat * (driver_gps_a.lon - start_line_a.lon) - gps_s2.lon * (driver_gps_a.lat - start_line_a.lat)) / \
        (-gps_s2.lat * gps_s1.lon + gps_s1.lat * gps_s2.lon)

    if not (0 <= s <= 1 and 0 <= t <= 1):
        # Intersection not detected.
        return False, GPSData()

    gps_result = GPSData(lat=driver_gps_a.lat + (t * gps_s1.lat), lon=driver_gps_a.lon + (t * gps_s1.lon))

    distance_a = distance(driver_gps_a.get_coordinate_as_tuple(), gps_result.get_coordinate_as_tuple()).meters
    distance_b = distance(driver_gps_b.get_coordinate_as_tuple(), gps_result.get_coordinate_as_tuple()).meters

    gps_result.timestamp = driver_gps_a.timestamp + abs(driver_gps_b.timestamp - driver_gps_a.timestamp) * \
                           distance_a / (distance_a + distance_b)

    return True, gps_result