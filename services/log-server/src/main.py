import asyncio

from overlord.log import log

import log_api
import grpc_api


async def main():
    message_queue = asyncio.Queue()

    log.info("log-server starting")

    await log_api.start_log_server(message_queue)

    await asyncio.gather(*[
        log_api.process_messages(message_queue),
        grpc_api.start()
    ])


if __name__ == '__main__':
    asyncio.run(main())
