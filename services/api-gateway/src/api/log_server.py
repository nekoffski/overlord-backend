
import grpc

from overlord import proto

LOG_SERVER_HOST = 'log-server'
LOG_SERVER_PORT = 5555


class LogServerProxy(proto.LogServerServicer):
    async def rotate(
        self,
        request: proto.RotateRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.RotateResponse:
        async with grpc.aio.insecure_channel(f"{LOG_SERVER_HOST}:{LOG_SERVER_PORT}") as channel:
            client = proto.LogServerStub(channel)
            return await client.rotate(request)

    async def getLogs(
        self,
        request: proto.GetLogsRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.GetLogsResponse:
        async with grpc.aio.insecure_channel(f"{LOG_SERVER_HOST}:{LOG_SERVER_PORT}") as channel:
            client = proto.LogServerStub(channel)
            return await client.getLogs(request)


def register_log_server_proxy(server):
    proto.add_LogServerServicer_to_server(LogServerProxy(), server)
