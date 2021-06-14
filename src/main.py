'''Goals are to use:
FLUENT PYTHON
- a decorator
- tdd or bdd??  
- OOP where broken into classes and each function is documented and has 1 objective 
- a dunder method ✅
- a generator
- dependency injection
- grpc
- dockerize it
- a oop uml diagram
'''

import asyncio
from data_classes.Starlink import Constellation
from data_classes.NOAA import SpaceWeather
from utils.logging import get_logger


async def fetch_constellation():
    await constellation.build()

async def fetch_data_loop(weather):
    while True:
        await asyncio.gather(
            weather.fetch_magnetosphere(),
            weather.fetch_plasma(),
            weather.run_weather(),
            asyncio.sleep(90)
        )

if __name__ == '__main__':
    logger = get_logger('Main')

    weather = SpaceWeather()
    constellation = Constellation(subscribe=weather)
    constellation.build()

    logger.info('Starting event loop')
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(fetch_data_loop(weather))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

    logger.info('Closing event loop')


