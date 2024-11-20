
from typing import Awaitable, Callable, Optional

import grpc

from overlord.log import log
from overlord import proto


class RequestLogger(grpc.aio.ServerInterceptor):
    async def intercept_service(
        self,
        continuation: Callable[
            [grpc.HandlerCallDetails], Awaitable[grpc.RpcMethodHandler]
        ],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        log.debug("Received grpc request: {}", handler_call_details.method)
        return await continuation(handler_call_details)


async def start():
    listen_addr = "[::]:5555"
    log.info("Starting grpc server on: {}", listen_addr)

    server = grpc.aio.server(interceptors=(RequestLogger(),))
    server.add_insecure_port(listen_addr)

    proto.register_pinger_service(server)

    await server.start()
    await server.wait_for_termination()
