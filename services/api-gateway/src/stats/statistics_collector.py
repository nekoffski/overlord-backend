import asyncio

from .statistics_proxy import StatisticsProxy
from .service import Service

from overlord.log import log
from overlord import cfg


DEFAULT_INTERVAL = 0.5


class StatisticsCollector(object):
    def __init__(self, interval=DEFAULT_INTERVAL):
        self.interval = interval
        self.services = [
            Service('Log Server', cfg.LOG_SERVER_HOST,
                    cfg.LOG_SERVER_GRPC_PORT),
            Service('Device Gateway', cfg.DEVICE_GATEWAY_HOST,
                    cfg.DEVICE_GATEWAY_GRPC_PORT),
            Service('Yeelight Connector', cfg.YEELIGHT_CONNECTOR_HOST,
                    cfg.YEELIGHT_CONNECTOR_GRPC_PORT)
        ]

    async def start(self):
        log.info("Statistics collector starting")
        log.info("Gathering stats every: {}s", self.interval)

        while True:
            await asyncio.gather(*[
                service.ping() for service in self.services
            ])
            await asyncio.sleep(self.interval)

    def get_proxy(self) -> StatisticsProxy:
        return StatisticsProxy(self.services)
