
import grpc

from overlord import proto, cfg
from overlord.log import log_errors


class DeviceGatewayProxy(proto.DeviceGatewayServicer):
    endpoint = f"{cfg.DEVICE_GATEWAY_HOST}:{cfg.DEVICE_GATEWAY_GRPC_PORT}"

    @log_errors()
    async def discover_devices(
        self,
        request: proto.DiscoverDevicesRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        async with grpc.aio.insecure_channel(self.endpoint) as channel:
            return await proto.DeviceGatewayStub(channel).discover_devices(request)

    @log_errors()
    async def get_devices(
        self,
        request: proto.GetDevicesRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.Devices:
        async with grpc.aio.insecure_channel(self.endpoint) as channel:
            return await proto.DeviceGatewayStub(channel).get_devices(request)

    @log_errors()
    async def toggle(
        self,
        request: proto.ToggleRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        async with grpc.aio.insecure_channel(self.endpoint) as channel:
            return await proto.DeviceGatewayStub(channel).toggle(request)

    @log_errors()
    async def set_rgb(
        self,
        request: proto.SetRgbRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        async with grpc.aio.insecure_channel(self.endpoint) as channel:
            return await proto.DeviceGatewayStub(channel).set_rgb(request)

    @log_errors()
    async def set_hsv(
        self,
        request: proto.SetHsvRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        async with grpc.aio.insecure_channel(self.endpoint) as channel:
            return await proto.DeviceGatewayStub(channel).set_hsv(request)

    @log_errors()
    async def set_brightness(
        self,
        request: proto.SetBrightnessRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        async with grpc.aio.insecure_channel(self.endpoint) as channel:
            return await proto.DeviceGatewayStub(channel).set_brightness(request)


def register_device_gateway_proxy(server):
    proto.add_DeviceGatewayServicer_to_server(
        DeviceGatewayProxy(), server)
