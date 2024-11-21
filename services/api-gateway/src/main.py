import asyncio

from overlord.log import log, setup_logger

import api
import stats


async def main():
    setup_logger(service_name='overlord-api-gateway')
    log.info("Service starting")

    stats_collector = stats.StatisticsCollector()

    await asyncio.gather(*[
        stats_collector.start(),
        api.start(stats_collector.get_proxy())
    ])


if __name__ == '__main__':
    asyncio.run(main())
