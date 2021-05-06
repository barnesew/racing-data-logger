import time


def get_precise_timestamp():
    # Returns high-precision timestamp in seconds
    return time.time_ns() / (10 ** 9)


def get_log_name_timestamp():
    return time.strftime("(%Y-%m-%d)_(%H.%M.%S)", time.gmtime())
