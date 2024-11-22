import asyncio

from .statistics_proxy import StatisticsProxy
from .service import Service

from overlord.log import log


DEFAULT_INTERVAL = 0.5


class StatisticsCollector(object):
    def __init__(self, interval=DEFAULT_INTERVAL):
        self.interval = interval
        self.services = [
            Service('Log Server', 'log-server', 5555),
            Service('Mi Proxy', 'mi-proxy', 5555)
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
