
import grpc

from loguru import logger as log
from overlord import proto, interceptor

GRPC_API_PORT = 5555


async def start():
    listen_addr = f"[::]:{GRPC_API_PORT}"
    log.info("Starting grpc server on: {}", listen_addr)

    server = grpc.aio.server(interceptors=(
        interceptor.RequestLogger(log, filters=['ping']),))
    server.add_insecure_port(listen_addr)

    proto.register_pinger_service(server)

    await server.start()
    await server.wait_for_termination()
