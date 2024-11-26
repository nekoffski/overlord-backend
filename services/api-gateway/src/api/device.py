
import grpc

from overlord import proto, cfg


class DeviceGatewayProxy(proto.DeviceGatewayServicer):
    endpoint = f"{cfg.DEVICE_GATEWAY_HOST}:{cfg.DEVICE_GATEWAY_GRPC_PORT}"

    async def discover_devices(
        self,
        request: proto.DiscoverDevicesRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.Devices:
        async with grpc.aio.insecure_channel(self.endpoint) as channel:
            return await proto.DeviceGatewayStub(channel).discover_devices(request)

    async def get_devices(
        self,
        request: proto.GetDevicesRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.Devices:
        async with grpc.aio.insecure_channel(self.endpoint) as channel:
            return await proto.DeviceGatewayStub(channel).get_devices(request)

    async def toggle(
        self,
        request: proto.ToggleRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.AckResponse:
        async with grpc.aio.insecure_channel(self.endpoint) as channel:
            return await proto.DeviceGatewayStub(channel).toggle(request)


def register_device_gateway_proxy(server):
    proto.add_DeviceGatewayServicer_to_server(
        DeviceGatewayProxy(), server)
