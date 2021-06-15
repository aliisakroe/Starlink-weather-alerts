!! This in an exploratory project (for fun!) and should not be used for scientific purposes, as it has not been
peer-reviewed by space weather nor satellite experts.

#### PREMISE:
Starlink (LEO) satelites are threatened by solar storms which may cause interference in communications
and increased orbital decay.
    https://www.swpc.noaa.gov/impacts/satellite-communications
    https://www.swpc.noaa.gov/impacts/satellite-drag
    https://doi.org/10.1016/j.asr.2017.12.034

This project will use the real-time Bz coordinate of Earth's magnetosphere to monitor solar storms.
A negative Bz coordinate indicates a solar storm that can affect satellites. More research is needed for the threshold
 of this negative value.

#### Data
It uses:
- TLE data of Starlink locations
- NOAA Space Weather solar winds endpoint
- NOAA Space Weather magnetosphere endpoint
- sqlite databases to store these values for storm lookups

#### Software Architecture
This program utilizes an observer pattern to register callback functions to warn satellites to ready their thrusters.
![alt text](https://github.com/aliisakroe/Starlink-weather-alerts/blob/main/uml.pdf?raw=true)

#### Usage
This can be pulled as a docker image. There is no console output, but an alert.log file will be written showing the
method calls and (too frequent/likely inaccurate) storms that call t

#### Notes
This project uses concurrent api calls though this is not necessary for the fast response and small
amount of data from these endpoints. This is an exercise for the programmer because not all api endpoints will be so
generous and consistent.

#### Future Directions
With more atmospheric research this analysis could be restructured for storm prediction in the future, for thruster
fuel planning defore launch.

#### Known improvements
-- Data may be fetched mutliple times from API source, causing multiple callbacks per storm
-- Only alert truly vulnerable satellites based on location between Earth and Sun, rather than full constellation
-- Continue adding unit and feature tests for code coverage and quality assurance
-- More error logging

