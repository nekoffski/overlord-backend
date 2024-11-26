from typing import Awaitable, Callable, Optional

import grpc


class RequestLogger(grpc.aio.ServerInterceptor):
    def __init__(self, log, filters):
        self.log = log
        self.filters = filters

    def should_skip(self, method_name):
        for f in self.filters:
            if f in method_name:
                return True
        return False

    async def intercept_service(
        self,
        continuation: Callable[
            [grpc.HandlerCallDetails], Awaitable[grpc.RpcMethodHandler]
        ],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        if not self.should_skip(handler_call_details.method):
            self.log.debug(
                "Received grpc request: {}", handler_call_details.method)
        return await continuation(handler_call_details)


class ErrorLogger(grpc.aio.ServerInterceptor):
    def __init__(self, log):
        self.log = log

    async def intercept_service(
        self,
        continuation: Callable[
            [grpc.HandlerCallDetails], Awaitable[grpc.RpcMethodHandler]
        ],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        try:
            return await continuation(handler_call_details)
        except Exception as e:
            log.error("{} - exception caught while handling request: {}",
                      handler_call_details.method, str(e))
            raise e
