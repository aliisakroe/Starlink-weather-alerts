'''Starlink makes this data publicly available on the site https://www.space-track.org/#publicFiles
TLE data is a telemetry format of form

Satellite
Name
TLE #todo
TLE

The TLE class parses each file into Satelite objects'''

import os
import re
from itertools import izip_longest

class TLE_file():
    def __init__(self, file, data_dir='./starlink_data/'):
        self.num_satellites = 0
        self.path = os.path.join(data_dir, file)

    def _get_satellite_name(self, str):
        '''Confirm TLE is in proper format, line 1'''
        assert re.match(r'[a-zA-Z ]+', str) #todo error check
        return str

    def _get_tle(self, str):
        '''Confirm TLE is in proper format, lines 2&3'''
        assert re.fullmatch(r'[0-9 ]+', str) != None
        return str

    def _parse_satellite(self, lines):
        n, t1, t2 = lines
        name = self._get_satellite_name(n)
        tle1, tle2 = self._get_tle(t1), self._get_tle(t2)
        return Satellite(name, tle1, tle2)

    def _grouper(self, iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return izip_longest(*args, fillvalue=fillvalue)

    def read_data(self):
        try:
            with open(self.path, 'r') as f:

                lines = f.readlines()
                satellite_array = []

                for i, group in enumerate(self._grouper(lines, 3)):
                    if i == 0:
                        pass #title info
                    elif i % 1 == 0:
                        satellite = self._parse_satellite(group)
                        satellite_array.append(satty)

            self.num_satellites = len(satellite_array)
            return satellite_array

        except Exception as m : #todo discover better exception codes
           raise m

class Satellite():  # todo refactor to the real starlink name
    def __init__(self, _name, _line2, _line3):
        name = _name