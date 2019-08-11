import sys
import logging
from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler
from aiologger.handlers.streams import AsyncStreamHandler
import asyncio

from aiologger.handlers.files import AsyncFileHandler


async def configure_logging():

    loop = asyncio.get_event_loop()
    logger = Logger(loop=loop, level=logging.DEBUG)

    file_handler = AsyncFileHandler(
        filename="./debug.log",
        mode="w+",
        loop=loop
        #"%(levelname)s - %(asctime)s - %(message)s"
    )
    logger.add_handler(file_handler)

    stream_handler = AsyncStreamHandler(
        stream=sys.stdout,
        level=logging.INFO,
        formatter=logging.Formatter("%(levelname)s - %(message)s"),
        loop=loop
    )
    logger.add_handler(stream_handler)

    logging.debug("Debug logger configured.")
