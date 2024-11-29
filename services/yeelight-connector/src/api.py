
import grpc

from overlord.log import log, log_errors
from overlord import proto, interceptor, cfg

from bulb_manager import BulbManager


class YeelightConnector(proto.YeelightConnectorServicer):
    def __init__(self, bulb_manager: BulbManager):
        self.bulb_manager = bulb_manager

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
        log.debug("Received toggle request for bulbs: {}", request)
        for id in request.ids:
            await self.bulb_manager.get_bulb(bulb_id=id).toggle()
        return proto.AckResponse()

    @log_errors()
    async def set_rgb(
        self,
        request: proto.SetRgbRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        log.debug("Received set_rgb request for bulbs: {}", request)
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
        log.debug("Received set_hsv request for bulbs: {}", request)
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
        log.debug("Received set_brightness request for bulbs: {}", request)
        for id in request.ids:
            await self.bulb_manager.get_bulb(bulb_id=id).set_brightness(
                request.brightness
            )
        return proto.AckResponse()


def register_yeelight_connector_service(server, bulb_manager: BulbManager):
    proto.add_YeelightConnectorServicer_to_server(
        YeelightConnector(bulb_manager), server)


async def start(bulb_manager: BulbManager):
    listen_addr = f"[::]:{cfg.YEELIGHT_CONNECTOR_GRPC_PORT}"
    log.info("Starting grpc server on: {}", listen_addr)

    server = grpc.aio.server(
        interceptors=(
            interceptor.RequestLogger(log, filters=['ping', "get_"]),))
    server.add_insecure_port(listen_addr)

    proto.register_pinger_service(server)
    register_yeelight_connector_service(server, bulb_manager)

    await server.start()
    await server.wait_for_termination()
