import asyncio
import socket

from typing import List

from .device_info import DeviceInfo
from .bulb import Bulb


YEELIGHT_MULTICAST_IP = '239.255.255.250'
YEELIGHT_MULTICAST_PORT = 1982
YEELIGHT_MULTICAST_ADDR = (YEELIGHT_MULTICAST_IP, YEELIGHT_MULTICAST_PORT)


def _broadcast_request(request: str) -> List[str]:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    s.sendto(request.encode(), YEELIGHT_MULTICAST_ADDR)
    s.settimeout(1)

    def read_responses() -> str:
        while True:
            try:
                data, _ = s.recvfrom(1024)
                if data:
                    yield data.decode()
            except socket.timeout as e:
                break
    return list(read_responses())


def _parse_headers(payload: str) -> dict:
    headers = {}
    for line in payload.split('\r\n'):
        if ':' not in line:
            continue
        index = line.index(':')
        key, value = line[:index].strip(), line[index + 1:].strip()
        headers[key.lower()] = value
    return headers


def _parse_device_response(payload: str) -> DeviceInfo:
    headers = _parse_headers(payload)
    host, port = headers['location'].split('//')[1].split(':')

    return DeviceInfo(
        id=int(headers['id'], base=16), model=headers['model'],
        name=headers['name'], host=host, port=int(port),
        actions=headers['support'].split(' '))


async def _discover_devices(device_type: str) -> List[DeviceInfo]:
    discover_request = '\r\n'.join([
        'M-SEARCH * HTTP/1.1',
        f'HOST: {YEELIGHT_MULTICAST_IP}:{YEELIGHT_MULTICAST_PORT}',
        'MAN: "ssdp:discover"',
        f'ST: {device_type}'
    ])
    payloads = await asyncio.to_thread(_broadcast_request, discover_request)
    devices = map(_parse_device_response, payloads)
    return list(set(devices))  # there could be duplicates


async def discover_bulbs() -> List[DeviceInfo]:
    devices = await _discover_devices(device_type="wifi_bulb")
    bulbs = list(map(lambda info: Bulb(info), devices))

    for bulb in bulbs:
        await bulb.connect()
    return bulbs
