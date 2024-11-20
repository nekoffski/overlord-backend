from typing import Awaitable, Callable, Optional

import grpc


class RequestLogger(grpc.aio.ServerInterceptor):
    def __init__(self, log):
        self.log = log

    async def intercept_service(
        self,
        continuation: Callable[
            [grpc.HandlerCallDetails], Awaitable[grpc.RpcMethodHandler]
        ],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        self.log.debug(
            "Received grpc request: {}", handler_call_details.method)
        return await continuation(handler_call_details)
