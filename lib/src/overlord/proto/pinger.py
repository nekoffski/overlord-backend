from .ping_pb2_grpc import *
from .ping_pb2 import *


class PingerService(PingerServicer):
    async def ping(
        self,
        request: PingRequest,
        context: grpc.aio.ServicerContext,
    ) -> PingResponse:
        response = PingResponse()
        response.timestamp.GetCurrentTime()
        return response


def register_pinger_service(server):
    add_PingerServicer_to_server(PingerService(), server)
