import asyncio
import os
import datetime
import shutil
import aiofiles
import sanic

from sanic.response import text, empty
from aiofiles.os import wrap
from loguru import logger as log


WEB_API_PORT = int(os.getenv('WEB_API_PORT', '5551'))
LOG_API_PORT = int(os.getenv('LOG_API_PORT', '5552'))
LOG_DIRECTORY = f'{os.getcwd()}/log'
LOG_FILE = f'{LOG_DIRECTORY}/logs.txt'


copy_file = wrap(shutil.copyfile)


async def clear_file(path: str):
    async with aiofiles.open(path, 'w'):
        pass


async def rotate_log_file():
    current_time = str(datetime.datetime.now()).replace(' ', '_')
    archive_log_file = f'{LOG_DIRECTORY}/{current_time}.txt'

    await copy_file(LOG_FILE, archive_log_file)
    await clear_file(LOG_FILE)


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
        lambda: LogProtocol(message_queue), local_addr=('0.0.0.0', LOG_API_PORT))


async def drain_message_queue(message_queue: asyncio.Queue):
    async with aiofiles.open(LOG_FILE, 'a') as f:
        while not message_queue.empty():
            message = await message_queue.get()
            print(message)
            await f.write(message)


async def process_messages(message_queue: asyncio.Queue):
    if not os.path.isdir(LOG_DIRECTORY):
        os.mkdir(LOG_DIRECTORY)

    max_log_file_size_mb = 128

    def to_megabytes(size):
        return size / (1024 * 1024)

    interval = 0.1

    while True:
        if not message_queue.empty():
            await drain_message_queue(message_queue)

        # TODO: use crontab
        def should_rotate():
            return os.path.isfile(LOG_FILE) and to_megabytes(
                os.stat(LOG_FILE).st_size) > max_log_file_size_mb

        if should_rotate():
            await rotate_log_file()

        await asyncio.sleep(interval)


def tail_log_file(file_content: str, lines: int) -> str:
    file_lines = list(filter(lambda x: len(x) > 0, file_content.split('\n')))
    return '\n'.join(file_lines[-lines:])


def register_endpoints(app: sanic.Sanic):
    @app.get('/')
    async def get_log_file_endpoint(request):
        async with aiofiles.open(LOG_FILE, 'r+') as f:
            log_file_content = await f.read()

            if 'tail' in request.args:
                lines_to_return = int(request.args.get('tail'))
                return text(tail_log_file(log_file_content, lines_to_return))
            return text(log_file_content)

    @app.post('/rotate')
    async def rotate_log_file_endpoint(_):
        await rotate_log_file()
        return empty(status=201)


async def start_http_server():
    if not os.path.isfile(LOG_FILE):
        open(LOG_FILE, 'a').close()

    log.info("starting sanic web server")
    app = sanic.Sanic(name='lune-log-server')

    register_endpoints(app)

    server = await app.create_server(
        '0.0.0.0', WEB_API_PORT, return_asyncio_server=True)

    await server.startup()
    await server.start_serving()


async def main():
    message_queue = asyncio.Queue()

    log.info("log-server starting")

    await start_http_server()
    await start_log_server(message_queue)
    await process_messages(message_queue)


if __name__ == '__main__':
    asyncio.run(main())
