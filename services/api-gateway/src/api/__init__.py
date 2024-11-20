import grpc

from overlord.log import log
from overlord import proto, interceptor


async def start():
    listen_addr = "[::]:5555"
    log.info("Starting grpc server on: {}", listen_addr)

    server = grpc.aio.server(interceptors=(interceptor.RequestLogger(log),))
    server.add_insecure_port(listen_addr)

    proto.register_pinger_service(server)

    await server.start()
    await server.wait_for_termination()
