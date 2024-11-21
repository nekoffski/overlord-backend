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
            Service('Mi Proxy', 'mi-proxy', 1337)
        ]

    async def start(self):
        log.info("Statistics collector starting")

        while True:
            log.debug("Pinging services")
            await asyncio.gather(*[
                service.ping() for service in self.services
            ])
            await asyncio.sleep(self.interval)

    def get_proxy(self) -> StatisticsProxy:
        return StatisticsProxy(self.services)
