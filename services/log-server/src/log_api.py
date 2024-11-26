
import asyncio
import os
import aiofiles

import utils

from loguru import logger as log
from overlord import cfg


class LogProtocol(asyncio.DatagramProtocol):
    def __init__(self, message_queue: asyncio.Queue):
        super().__init__()
        self.message_queue = message_queue

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        self.message_queue.put_nowait(data.decode('utf-8'))


async def start_log_server(message_queue: asyncio.Queue):
    loop = asyncio.get_event_loop()

    log.info("starting datagram log endpoint")

    await loop.create_datagram_endpoint(
        lambda: LogProtocol(message_queue), local_addr=(cfg.LOG_SERVER_HOST, cfg.LOG_SERVER_LOGGER_PORT))


async def drain_message_queue(message_queue: asyncio.Queue):
    async with aiofiles.open(utils.LOG_FILE, 'a') as f:
        while not message_queue.empty():
            message = await message_queue.get()
            await f.write(message)


async def process_messages(message_queue: asyncio.Queue):
    if not os.path.isdir(utils.LOG_DIRECTORY):
        os.mkdir(utils.LOG_DIRECTORY)

    max_log_file_size_mb = 128

    def to_megabytes(size):
        return size / (1024 * 1024)

    interval = 0.1

    while True:
        if not message_queue.empty():
            await drain_message_queue(message_queue)

        # TODO: use crontab
        def should_rotate():
            return os.path.isfile(utils.LOG_FILE) and to_megabytes(
                os.stat(utils.LOG_FILE).st_size) > max_log_file_size_mb

        if should_rotate():
            await rotate_log_file()

        await asyncio.sleep(interval)
