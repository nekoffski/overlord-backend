import asyncio

from overlord.log import log, setup_logger

import api


async def main():
    setup_logger(service_name='overlord-device-gateway')
    log.info("Service starting")

    await api.start()


if __name__ == '__main__':
    asyncio.run(main())
