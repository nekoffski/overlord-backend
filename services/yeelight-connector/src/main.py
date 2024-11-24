import asyncio

# from overlord.log import log, setup_logger

# import api


from yeelight import discover_bulbs


async def main():
    bulbs = await discover_bulbs()

    for bulb in bulbs:
        await bulb.toggle()

    await asyncio.sleep(5)

    for bulb in bulbs:
        await bulb.shutdown()

    # print(bulbs)

    # setup_logger(service_name='overlord-yeelight-connector')
    # log.info("Service starting")

    # await api.start()


if __name__ == '__main__':
    asyncio.run(main())
