import sys
import logging


def configure_logging():

    logging.getLogger().handlers = []

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_formatter = logging.Formatter("%(levelname)s - %(message)s")
    stdout_handler.setFormatter(stdout_formatter)

    file_handler = logging.FileHandler(
        filename="./debug.log",
        mode="w+"
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().addHandler(stdout_handler)
    logging.getLogger().addHandler(file_handler)

    logging.info("Debug logger configured.")
