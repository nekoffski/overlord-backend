
import grpc
import aiofiles

from loguru import logger as log
from overlord import proto, interceptor, cfg

import utils


class LogServer(proto.LogServerServicer):
    async def rotate(
        self,
        request: proto.RotateRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.RotateResponse:
        await utils.rotate_log_file()
        return proto.RotateResponse()

    async def get_logs(
        self,
        request: proto.GetLogsRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.GetLogsResponse:
        lines = []
        async with aiofiles.open(utils.LOG_FILE, 'r+') as f:
            file = await f.read()
            lines = list(filter(lambda s: len(s) > 0, file.split('\n')))
        return proto.GetLogsResponse(logs=lines[-50:])


def register_log_server(server):
    proto.add_LogServerServicer_to_server(LogServer(), server)


async def start():
    listen_addr = f"[::]:{cfg.LOG_SERVER_GRPC_PORT}"
    log.info("Starting grpc server on: {}", listen_addr)

    server = grpc.aio.server(interceptors=(
        interceptor.RequestLogger(log, filters=['ping']),))
    server.add_insecure_port(listen_addr)

    proto.register_pinger_service(server)
    register_log_server(server)

    await server.start()
    await server.wait_for_termination()
