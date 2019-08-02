import time


def get_formatted_timestamp():
    # Returns timestamp such as: "2019-01-23 10:45 UTC"
    return time.strftime("%y-%m-%d %H:%d:%S %Z", time.gmtime())


def get_precise_timestamp():
    # Returns high-precision timestamp in seconds
    return time.time_ns() / (10 ** 9)
