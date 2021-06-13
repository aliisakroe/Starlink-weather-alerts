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


from Starlink import TLE_file, Satellite
from NOAA_SolarWind import Magnetosphere, Plasma


if __name__ == '__main__':
    #todo for file in dir, or api to go out and call it good place for a generator
    #todo run for single file

    tle = TLE_file('MEME_44713_STARLINK-1007_1630208_Operational_1307758111_UNCLASSIFIED.txt')
    satellites = tle.read_data()
    print(tle.num_satellites)


