'''Starlink makes this data publicly available on the site https://www.space-track.org/#publicFiles
TLE data is a telemetry format of form

Satellite
Name
TLE #todo
TLE

The TLE class parses each file into Satelite objects'''

import os
import re
import requests
from itertools import zip_longest

class TLE_data():

    num_satellites = 0
    raw_data = None

    def __init__(self):
        self.raw_data = self.fetch()
        self.satellite_array = self.parse_data(self.raw_data)

    def fetch(self, url='https://celestrak.com/NORAD/elements/starlink.txt'): #url='https://celestrak.com/NORAD/elements/starlink.txt'):
        print("Fetching TLE data")
        try:
            tles = requests.get(url)
            assert tles.status_code == 200
            print("Fetch successful")
        except Exception:  #todo
            raise Exception
        return self._parse_data(tles.text)  # todo check if return before or after except statement

    def _parse_name(self, str):
        '''Confirm TLE is in proper format, line 1'''
        if re.match(r'FALCON 9|CAPELLA|TYVAK', str) != None:
            return
        name = re.match(r'STARLINK-\d+', str) #todo error check
        assert name != None, str
        return name

    def _parse_satellite(self, lines):
        n, t1, t2 = lines
        if n != '':
            name = self._parse_name(n)
            if name != None:
                return Satellite(name, t1, t2)

    def _grouper(self, n, iterable, fillvalue=None):
        "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)

    def _parse_data(self, data):
        print("Parsing data")
        lines = data.split('\n')

        satellite_array = []
        for group in self._grouper(3, lines):
            satellite = self._parse_satellite(group)
            satellite_array.append(satellite)

        self.num_satellites = len(satellite_array)
        return satellite_array

    def get_num_satellites(self):
        return self.num_satellites

class Satellite():  # todo refactor to the real starlink name
    name = None
    catalog_number = None
    classification = None
    launch_year = None
    launch_number = None
    launch_piece = None
    epoch_year = None
    epoch = None
    ballistic_coefficient = None
    mean_motion = None
    radiation_drag_coefficient = None
    inclination = None
    right_ascention_ascending_node = None
    eccentricity = None
    argment_of_perigee = None
    mean_anomaly = None
    mean_motion = None
    revolutions = None

    def __init__(self, _name, _line1, _line2):
        self.name = _name
        self._parse_line1(_line1)
        self._parse_line2(_line2)

    def _parse_line1(self, str):
        m = re.match(r'(\d) (\d+\S+)\s+(\d+\S+)\s+([\d.]+)\s+([\d.-]+)\s+([\d-]+)\s+([\d-]+)\s+(\d)\s+(\d+)', str)
        assert m != None, str
        self.catalog_number = m.group(1)
        self.classification = m.group(2)
        self.launch_year = m.group(3)
        self.launch_number = m.group(4)
        self.epoch_year = m.group(5)
        self.epoch = m.group(6)
        self.ballistic_coefficient = m.group(7)
        self.mean_motion = m.group(8)
        self.radiation_drag_coefficient = m.group(0) #todo


    def _parse_line2(self, str):
        m = re.match(r'\d (\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', str)
        assert m != None, str
        self.inclination = m.group(1)
        self.right_ascention_ascending_node = m.group(2)
        self.eccentricity = m.group(3)
        self.argment_of_perigee = m.group(4)
        self.mean_anomaly = m.group(5)
        self.mean_motion = m.group(6)
        self.revolutions = m.group(7) #todo


class Constellation(TLE_data):
    #todo generator of number of sattelites to grab
    def __init__(self):
        self.satellite_array = self.fetch()
        print(self.num_satellites)


