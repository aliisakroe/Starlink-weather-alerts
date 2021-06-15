'''Run this file as `python main.py` to run program.
After initializing a Starlink Constellation this program fetches weather data from 2 NOAA apis in coroutines
Alert.log will show mathods called, including actions after storm events.

It will continure to fetch new weather data every minute until the user manually terminates the program.'''

import asyncio
from data_classes.Starlink import Constellation
from data_classes.NOAA import SpaceWeather
from utils.logging import get_logger

async def fetch_constellation():
    '''Returns a Constellation object
    after fetching fetching Starlink TLE data
    '''
    await constellation.build()

async def fetch_data_loop(weather):
    '''Loop continues to fetch weather data
    and check for storms every minute until
     user termination'''
    while True:
        await asyncio.gather(
            weather.fetch_magnetosphere(),
            weather.fetch_plasma(),
            weather.run_weather(),
            asyncio.sleep(90)
        )

if __name__ == '__main__':
    logger = get_logger('Main')

    #Initialize constellation
    weather = SpaceWeather()
    constellation = Constellation(subscribe=weather)
    constellation.build()

    #Continuous fetch real-time space weather data
    logger.info('Starting event loop')
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(fetch_data_loop(weather))
        loop.run_forever()

    #User termination
    except KeyboardInterrupt:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
    logger.info('Closing event loop')


