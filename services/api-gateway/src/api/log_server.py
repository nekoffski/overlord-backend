
import grpc

from overlord import proto, cfg


class LogServerProxy(proto.LogServerServicer):
    endpoint = f"{cfg.LOG_SERVER_HOST}:{cfg.LOG_SERVER_GRPC_PORT}"

    async def rotate(
        self,
        request: proto.RotateRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.RotateResponse:
        async with grpc.aio.insecure_channel(self.endpoint) as channel:
            client = proto.LogServerStub(channel)
            return await client.rotate(request)

    async def get_logs(
        self,
        request: proto.GetLogsRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.GetLogsResponse:
        async with grpc.aio.insecure_channel(self.endpoint) as channel:
            client = proto.LogServerStub(channel)
            return await client.get_logs(request)


def register_log_server_proxy(server):
    proto.add_LogServerServicer_to_server(LogServerProxy(), server)
