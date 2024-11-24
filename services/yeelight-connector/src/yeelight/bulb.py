import asyncio
import json

from typing import List, Tuple
from .device_info import DeviceInfo


class Bulb(object):
    def __init__(self, device_info: DeviceInfo):
        self.info = device_info
        self.reader = None
        self.writer = None
        self.reader_task = None
        self.next_message_id = 0

        required_actions = [

        ]

        for action in required_actions:
            if not self.info.supports_action(action):
                # TODO: throw error
                pass

    async def shutdown(self):
        self.writer.close()
        await self.writer.wait_closed()
        await self.reader_task

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(
            self.info.host, self.info.port)
        self.reader_task = asyncio.create_task(self._read_messages())

    async def toggle(self):
        await self._request('toggle',)

    async def _read_messages(self):
        while True:
            response = await self.reader.read(1024)
            if not response:
                break
            print(response.decode('utf-8'))

    async def _write(self, payload: str):
        self.writer.write(payload.encode('utf-8'))
        await self.writer.drain()

    async def _request(self, method: str, params: Tuple = None) -> int:
        if params is None:
            params = ()
        request = {
            'id': self.generate_id(),
            'method': method,
            'params': params
        }
        await self._write(json.dumps(request) + '\r\n')
        return request['id']

    def generate_id(self):
        MAX_MESSAGE_ID = 1 << 12

        self.next_message_id += 1
        if self.next_message_id >= MAX_MESSAGE_ID:
            self.next_message_id = 0
        return self.next_message_id
