import asyncio
import json

from typing import List, Tuple

from overlord.log import log
from overlord import proto

from .device_info import DeviceInfo


class Bulb(object):
    def __init__(self, device_info: DeviceInfo):
        self.info = device_info
        self.reader = None
        self.writer = None
        self.reader_task = None
        self.next_message_id = 0
        self.ident = f'Bulb[yeelight://{self.info.host}:{
            self.info.port}/{hex(self.info.id)}]'

        required_actions = [

        ]

        log.info("{} - created", self.ident)

        for action in required_actions:
            if not self.info.supports_action(action):
                # TODO: throw error
                pass

    async def shutdown(self):
        log.info("{} - shutting down", self.ident)
        self.writer.close()
        await self.writer.wait_closed()
        await self.reader_task

    def to_proto(self) -> proto.Device:
        return proto.Device(
            id=self.info.id, name=self.info.name
        )

    async def connect(self):
        log.info("{} - connecting to the bulb endpoint: {}/{}",
                 self.ident, self.info.host, self.info.port)
        self.reader, self.writer = await asyncio.open_connection(
            self.info.host, self.info.port)
        self.reader_task = asyncio.create_task(self._read_messages())

    async def toggle(self):
        await self._request('toggle')

    async def set_hsv(self, h: int, s: int, v: int, transition='smooth', duration=500):
        await self._request('set_hsv', params=[h, s, transition, duration])
        await self.set_brightness(brightness=v)

    async def set_rgb(self, r: int, g: int, b: int, transition='smooth', duration=500):
        # each color component represented by 1 byte, top byte is red and bottom byte is blue
        rgb = (r << 16) + (g << 8) + b
        await self._request('set_rgb', params=[rgb, transition, duration])

    async def set_brightness(self, brightness: int, transition='smooth', duration=500):
        await self._request('set_bright', params=[brightness, transition, duration])

    async def _read_messages(self):
        while True:
            response = await self.reader.read(1024)
            if not response:
                break
            response = response.decode('utf-8')
            log.debug("{} - received message: {}", self.ident, response)

    async def _write(self, payload: str):
        payload = payload.encode('utf-8')
        log.debug("{} - sending payload: {}", self.ident, payload)
        self.writer.write(payload)
        await self.writer.drain()

    async def _request(self, method: str, params: Tuple = None) -> int:
        if params is None:
            params = ()
        request = {
            'id': self.generate_id(),
            'method': method,
            'params': params
        }
        log.debug("{} - sending reqeust: {}", self.ident, request)
        await self._write(json.dumps(request) + '\r\n')
        return request['id']

    def generate_id(self):
        MAX_MESSAGE_ID = 1 << 12

        self.next_message_id += 1
        if self.next_message_id >= MAX_MESSAGE_ID:
            self.next_message_id = 0
        return self.next_message_id
