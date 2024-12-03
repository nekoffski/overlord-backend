import asyncio

from typing import List

from overlord.log import log
from overlord import proto

from yeelight import Bulb, discover_bulbs
from event import EventManager, EventProducer


class BulbManager(object):
    def __init__(self, event_manager: EventManager):
        self.bulbs = {}
        self.event_manager = event_manager

    async def discover(self):
        log.info("Looking for devices in local network")
        for bulb_info in await discover_bulbs():
            if bulb_info.id in self.bulbs:
                log.info("Bulb '{}' already stored, skipping", bulb_info.id)
                continue
            bulb = Bulb(bulb_info, self.event_manager.create_producer())
            log.info("Found bulb: {}, connecting...", bulb_info)
            await bulb.connect()
            self.bulbs[bulb_info.id] = bulb

    def get_bulb(self, bulb_id: int) -> Bulb | None:
        return self.bulbs.get(bulb_id)

    def get_bulbs_info(self) -> List[proto.Device]:
        return [bulb.to_proto() for bulb in self.bulbs.values()]
