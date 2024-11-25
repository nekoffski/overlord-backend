import asyncio

from overlord.log import log, setup_logger

import api


from yeelight import discover_bulbs
from bulb_manager import BulbManager


async def main():
    setup_logger(service_name='overlord-yeelight-connector')
    log.info("Service starting")

    bulb_manager = BulbManager()
    await api.start(bulb_manager)


if __name__ == '__main__':
    asyncio.run(main())
