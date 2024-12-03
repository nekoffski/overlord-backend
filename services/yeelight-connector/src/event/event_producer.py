import typing

from overlord.log import log
from overlord import proto


class EventProducer(object):
    def __init__(self, forward_event: typing.Callable[[proto.DeviceEvent], typing.NoReturn]):
        self.forward_event = forward_event

    async def emit(self, payload: dict, device_id: int):
        log.debug("Emitting payload: {}", payload)
        event = self._parse_event(payload, device_id)
        if not event:
            log.error("Could not parse event")
            return
        log.debug("Event parsed to: {}", str(event))
        await self.forward_event(event)

    def _parse_event(self, payload: dict, device_id: int) -> proto.DeviceEvent:
        if self._has_fields(payload, fields=['hue', 'sat', 'rgb']):
            event = proto.DeviceColorChanged(
                h=payload['hue'], s=payload['sat'])
            return proto.DeviceEvent(
                device_id=device_id, type=proto.DeviceEventType.COLOR_CHANGED, color_changed=event
            )
        elif self._has_fields(payload, fields=['power']):
            event = proto.DeviceStateChanged(state=payload['power'].upper())
            log.debug("{} - {}", payload['power'], event.state)
            return proto.DeviceEvent(
                device_id=device_id, type=proto.DeviceEventType.STATE_CHANGED, state_changed=event
            )
        elif self._has_fields(payload, fields=['bright']):
            event = proto.DeviceBrightnessChanged(
                brightness=payload['bright'])
            return proto.DeviceEvent(
                device_id=device_id, type=proto.DeviceEventType.BRIGHTNESS_CHANGED, brightness_changed=event
            )
        return None

    def _has_fields(self, payload: dict, fields: typing.List[str]) -> bool:
        return all([field in payload for field in fields])
