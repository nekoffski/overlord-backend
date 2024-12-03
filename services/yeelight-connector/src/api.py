
import grpc

from overlord.log import log, log_errors
from overlord import proto, interceptor, cfg

from bulb_manager import BulbManager
from event import EventConsumer, EventManager


class YeelightConnector(proto.YeelightConnectorServicer):
    def __init__(self, bulb_manager: BulbManager, event_manager: EventManager):
        self.bulb_manager = bulb_manager
        self.event_manager = event_manager

    @log_errors()
    async def discover_devices(
        self,
        request: proto.DiscoverDevicesRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        await self.bulb_manager.discover()
        return proto.AckResponse()

    @log_errors()
    async def get_devices(
        self,
        request: proto.GetDevicesRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.Devices:
        return proto.Devices(devices=self.bulb_manager.get_bulbs_info())

    @log_errors()
    async def toggle(
        self,
        request: proto.ToggleRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        log.debug("Received toggle request for bulbs: {}", request.ids)
        for id in request.ids:
            await self.bulb_manager.get_bulb(bulb_id=id).toggle()
        return proto.AckResponse()

    @log_errors()
    async def set_rgb(
        self,
        request: proto.SetRgbRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        log.debug("Received set_rgb request for bulbs: {}, r/g/b={}/{}/{}",
                  request.ids, request.r, request.g, request.b)
        for id in request.ids:
            await self.bulb_manager.get_bulb(bulb_id=id).set_rgb(
                request.r, request.b, request.b)
        return proto.AckResponse()

    @log_errors()
    async def set_hsv(
        self,
        request: proto.SetHsvRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        log.debug("Received set_hsv request for bulbs: {}, h/s/v={}/{}/{}",
                  request.ids, request.h, request.s, request.v)
        for id in request.ids:
            await self.bulb_manager.get_bulb(bulb_id=id).set_hsv(
                request.h, request.s, request.v)
        return proto.AckResponse()

    @log_errors()
    async def set_brightness(
        self,
        request: proto.SetBrightnessRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        log.debug("Received set_brightness request for bulbs: {}, brighntess={}",
                  request.ids, request.brightness)
        for id in request.ids:
            await self.bulb_manager.get_bulb(bulb_id=id).set_brightness(
                request.brightness
            )
        return proto.AckResponse()

    @log_errors()
    async def enable_music_mode(
        self,
        request: proto.EnableMusicModeRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        log.debug("Received enable_music_mode request for bulbs: {}, addr={}:{}",
                  request.ids, request.host, request.port)
        for id in request.ids:
            await self.bulb_manager.get_bulb(bulb_id=id).enable_music_mode(
                request.host, request.port)
        return proto.AckResponse()

    @log_errors()
    async def disable_music_mode(
        self,
        request: proto.DisableMusicModeRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        log.debug("Received disable_music_mode request for bulbs: {}", request.ids)
        for id in request.ids:
            await self.bulb_manager.get_bulb(bulb_id=id).disable_music_mode()
        return proto.AckResponse()

    async def listen_to_notifications(
        self,
        request: proto.StartNotificationStream,
        context: grpc.aio.ServicerContext,
    ) -> proto.DeviceEvent:
        log.debug("Streaming notifications to client")
        consumer = self.event_manager.create_consumer()
        try:
            while True:
                event = await consumer.wait_for_event()
                yield event
        except Exception as e:
            log.warn("Stream ended: {}", e)
            consumer.unregister()


def register_yeelight_connector_service(server, bulb_manager: BulbManager, event_consumer: EventConsumer):
    proto.add_YeelightConnectorServicer_to_server(
        YeelightConnector(bulb_manager, event_consumer), server)


async def start(bulb_manager: BulbManager, event_manager: EventManager):
    listen_addr = f"[::]:{cfg.YEELIGHT_CONNECTOR_GRPC_PORT}"
    log.info("Starting grpc server on: {}", listen_addr)

    server = grpc.aio.server(
        interceptors=(
            interceptor.RequestLogger(log, filters=['ping', "get_"]),))
    server.add_insecure_port(listen_addr)

    proto.register_pinger_service(server)
    register_yeelight_connector_service(server, bulb_manager, event_manager)

    await server.start()
    await server.wait_for_termination()
