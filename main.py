'''This is a program written for an interview with SpaceX Starlink. It is an exploratory project to show
fluency in python programming and should not be used for scientific purposes, as it has not been peer-reviewed
by space weather nor satellite experts.

PREMISE:
Starlink (LEO) satelites are threatened by solar storms which may cause interference in communications
and increased orbital decay.
    https://www.swpc.noaa.gov/impacts/satellite-communications
    https://www.swpc.noaa.gov/impacts/satellite-drag
    https://doi.org/10.1016/j.asr.2017.12.034

This project will use the real-time Bz coordinate of Earth's magnetosphere to monitor solar storms.
A negative Bz coordinate indicates a solar storm that can affect satellites in _____ regions.

This analysis can be extended for prediction in the future, for fuel planning before launch to adjust for
premature solar wind induced orbital decay.

It uses:
- TLE data of Starlink locations
- NOAA Space Weather solar winds

- AGI Simulation software under it's open source json library CesiumGS
To predict the likelihood of a fireball knocking out a portion of the constellation
(Especially as Starlink continues to scale...)
'''

'''Goals are to use:
FLUENT PYTHON
- a decorator
- tdd or bdd??  
- OOP where broken into classes and each function is documented and has 1 objective 
- a dunder method
- a generator
- dependency injection
- grpc
- dockerize it
- a oop uml diagram
'''

from Starlink import Constellation, get_logger
from NOAA import SpaceWeather
import asyncio

async def main():
    constellation = Constellation()
    weather = SpaceWeather()
    await asyncio.gather(constellation.build(), weather.fetch_plasma(), weather.fetch_magnetosphere())

if __name__ == '__main__':
    #todo real time fetching and print updates to console

    logger = get_logger('Main')
    logger.info('Starting event loop')
    asyncio.run(main())
    logger.info('Closing event loop')

