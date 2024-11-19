import asyncio

from overlord.log import log, setup_logger


async def main():
    setup_logger(service_name='overlord-api-gateway')
    log.info("Service starting")


if __name__ == '__main__':
    asyncio.run(main())
