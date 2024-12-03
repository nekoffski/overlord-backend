import asyncio
import typing

from uuid import uuid4 as uuid

from overlord import proto


class EventConsumer(object):
    def __init__(self, queue: asyncio.Queue, unregister: typing.Callable[[str], typing.NoReturn]):
        self.id = str(uuid)
        self.queue = queue
        self.unregister = unregister

    def get_id(self) -> str:
        return self.id

    def shutdown(self):
        self.unregister(self.id)

    async def wait_for_event(self) -> proto.DeviceEvent:
        return await self.queue.get()
