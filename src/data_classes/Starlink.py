'''Starlink makes this data publicly available on the site https://www.space-track.org/#publicFiles
TLE data is a telemetry format of form

Satellite
Name
TLE #todo
TLE

The TLE class parses each file into Satelite objects'''

import re
import requests
from itertools import zip_longest
import logging

def get_logger(name):
    logger = logging.getLogger(name)
    handler = logging.FileHandler('alert.log', 'a+')
    f = logging.Formatter('%(asctime)s - %(levelname)-10s - %(filename)s - %(funcName)s - %(message)s')
    handler.setFormatter(f)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

class TLEData():

    num_satellites = 0
    raw_data = None

    def __init__(self):
        self.logger = get_logger('Starlink.TLE_data')
        # self.raw_data = self.fetch()
        # self.satellite_array = self._parse_data(self.raw_data)


    def fetch(self, url='https://celestrak.com/NORAD/elements/starlink.txt'): #url='https://celestrak.com/NORAD/elements/starlink.txt'):
        self.logger.info("Fetching TLE Satellite data from Celestrak")
        try:
            r = requests.get(url)
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

        assert r.status_code == 200
        self.logger.info("TLE fetch successful")
        return self._parse_data(r.text)

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
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)

    def _parse_data(self, data):
        lines = data.split('\n')

        satellite_array = []
        for group in self._grouper(3, lines):
            satellite = self._parse_satellite(group)
            satellite_array.append(satellite)

        self.num_satellites = len(satellite_array)
        return satellite_array


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
        self.logger = get_logger('Starlink.Satellite')
        if _name == None:
            return
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

    def signal_thrusters(self):
        #todo to avoid orbital decay
        pass


class Constellation():
    satellite_array = []
    num_satellites = len(satellite_array)

    #todo generator of number of sattelites to grab
    def __init__(self, subscribe=None):
        self.logger = get_logger('Starlink.Constellation')
        self.logger.info('Initializing constellation')
        subscribe.magnetosphere.subscribe(self.broadcast_alert)

    def build(self):
        tle =  TLEData()
        self.satellite_array = tle.fetch()
        self.num_satellites = len(self.satellite_array)
        self.logger.info(f'Constellation assembled, {self.num_satellites} total satellites')

    def _get_vulnerable_satellites(self):
        #todo get all between sun and solar storm
        pass

    def broadcast_alert(self, e):
        # sat_array = self._get_vulnerable_satellites()
        for sat in self.satellite_array:
            if sat != None: #todo fix
                sat.signal_thrusters()
        self.logger.info(f'{self.num_satellites} satellite(s) have been alerted to ready their thrusters')



