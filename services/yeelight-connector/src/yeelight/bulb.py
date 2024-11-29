import asyncio
import json
import copy
from monotonic import monotonic
from typing import List, Tuple

from overlord.log import log
from overlord import proto

from .device_info import DeviceInfo


DEFAULT_SWITCH_DURATION = 2000
MAX_MESSAGE_ID = 1 << 8


class Bulb(object):

    def __init__(self, device_info: DeviceInfo):
        self.info = device_info
        self.reader = None
        self.writer = None
        self.reader_task = None
        self.next_message_id = 0
        self.ident = f'Bulb[yeelight://{self.info.host}:{
            self.info.port}/{hex(self.info.id)}]'

        self.responses = {}

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
        id = await self._request('toggle')

    async def set_hsv(self, h: int, s: int, v: int, transition='smooth', duration=DEFAULT_SWITCH_DURATION):
        id = await self._request('set_hsv', params=[h, s, transition, duration])
        await self._expect_ok(id)
        await self.set_brightness(brightness=v)

    async def set_rgb(self, r: int, g: int, b: int, transition='smooth', duration=DEFAULT_SWITCH_DURATION):
        # each color component represented by 1 byte, top byte is red and bottom byte is blue
        rgb = (r << 16) + (g << 8) + b
        id = await self._request('set_rgb', params=[rgb, transition, duration])
        await self._expect_ok(id)

    async def set_brightness(self, brightness: int, transition='smooth', duration=500):
        id = await self._request('set_bright', params=[brightness, transition, duration])
        await self._expect_ok(id)

    async def _wait_for_response(self, id: int, timeout: int = 5):
        deadline = monotonic() + timeout
        interval = 0.5
        while monotonic() < deadline:
            if id in self.responses:
                response = copy.deepcopy(self.responses[id])
                del self.responses[id]
                log.debug("Got response: {}", response)
                return response
            await asyncio.sleep(interval)
        return None

    async def _expect_ok(self, id: int):
        res = await self._wait_for_response(id=id)
        if res is None or 'ok' not in res:
            log.error("Expected result to be 'ok', got '{}' instead", res)
            raise RuntimeError("Failed expectation")
        log.debug("Got expected result")

    async def _read_messages(self):
        while True:
            response = await self.reader.read(1024)
            if not response:
                break
            response = json.loads(response.decode('utf-8'))
            log.debug("{} - received message: {}", self.ident, response)

            if 'id' in response and 'result' in response:
                self.responses[response['id']] = response['result']
            elif 'method' in response and 'params' in response:
                self._process_event(response['params'])

    def _process_event(self, event: dict):
        log.debug("{} - got event: {}", self.ident, event)

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
        self.next_message_id += 1
        if self.next_message_id >= MAX_MESSAGE_ID:
            self.next_message_id = 0
        return self.next_message_id
