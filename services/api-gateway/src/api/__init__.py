import grpc

from overlord.log import log
from overlord import proto, interceptor, cfg

from . import stats, log_server


async def start(stats_proxy):
    listen_addr = f"[::]:{cfg.API_GATEWAY_GRPC_PORT}"
    log.info("Starting grpc server on: {}", listen_addr)

    server = grpc.aio.server(interceptors=(
        interceptor.RequestLogger(log, filters=['ping', 'get_statistics']),))
    server.add_insecure_port(listen_addr)

    proto.register_pinger_service(server)
    stats.register_statistics_provider_service(server, stats_proxy)
    log_server.register_log_server_proxy(server)

    await server.start()
    await server.wait_for_termination()
