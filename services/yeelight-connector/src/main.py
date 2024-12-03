import asyncio

from overlord.log import log, setup_logger

import api

from event import EventManager
from yeelight import discover_bulbs
from bulb_manager import BulbManager


async def main():
    setup_logger(service_name='overlord-yeelight-connector')
    log.info("Service starting")

    event_manager = EventManager()
    bulb_manager = BulbManager(event_manager)

    await bulb_manager.discover()
    await api.start(bulb_manager, event_manager)


if __name__ == '__main__':
    asyncio.run(main())
