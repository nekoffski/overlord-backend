import asyncio
import typing

from overlord import proto

from .event_consumer import EventConsumer
from .event_producer import EventProducer


class EventManager(object):
    def __init__(self):
        self.queues: typing.Dict[str, asyncio.Queue] = {}

    def create_producer(self) -> EventProducer:
        return EventProducer(forward_event=lambda event: self._forward_event(event))

    def create_consumer(self) -> EventConsumer:
        q = asyncio.Queue()
        consumer = EventConsumer(
            queue=q, unregister=lambda id: self._unregister_consumer(id))
        self.queues[consumer.get_id()] = q
        return consumer

    async def _forward_event(self, event: proto.DeviceEvent):
        for q in self.queues.values():
            await q.put(event)

    def _unregister_consumer(self, id):
        if id in self.queues:
            del self.queues[id]  # FIXME: possible race condition
