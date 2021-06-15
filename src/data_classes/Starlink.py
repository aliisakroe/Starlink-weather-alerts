'''Starlink makes this data publicly available through partners
TLE data is a telemetry format of form

Name
(line1)
(line2)

The TLE class parses each file into Satellite objects and
The Constellation class contains all Satellite objects
'''

import re
from itertools import zip_longest
from src.data_classes.base_classes.api import API
from src.utils.logging import get_logger


STARLINK_URL='https://celestrak.com/NORAD/elements/starlink.txt'

class TLEData(API):
    '''Fetches TLEData and parses into Satellite objects
    '''
    num_satellites = 0
    raw_data = None

    def __init__(self):
        self.logger = get_logger('Starlink.TLE_data')

    def _parse_name(self, str):
        '''Only select STARLINK Satellites
        '''
        if re.match(r'FALCON 9|CAPELLA|TYVAK', str) != None:
            return
        name = re.match(r'STARLINK-\d+', str)
        assert name != None, str
        return name

    def _parse_satellite(self, lines):
        '''Create Satellite objects

        :parameter: lines: (str, str, str)
        '''
        n, t1, t2 = lines
        if n != '':
            name = self._parse_name(n)
            if name != None:
                return Satellite(name, t1, t2)

    def _grouper(self, iterable, n=3, fillvalue=None):
        '''Helper function to parse 3 lines at a time
        corresponding to a satellite
        '''
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)

    def _parse(self, data):
        '''Parse data returned from API and
        create Satellites and store in array'''
        lines = data.text.split('\n')

        satellite_array = []
        for group in self._grouper(lines):
            satellite = self._parse_satellite(group)
            satellite_array.append(satellite)

        self.num_satellites = len(satellite_array)
        return satellite_array


class Satellite():
    '''Class for each TLE Satellite element, parsing each field
    data can be used for future research
    '''
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
        '''Parse fields from line1
        '''
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
        '''Parse fields from line 2
        '''
        m = re.match(r'\d (\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', str)
        assert m != None, str
        self.inclination = m.group(1)
        self.right_ascention_ascending_node = m.group(2)
        self.eccentricity = m.group(3)
        self.argment_of_perigee = m.group(4)
        self.mean_anomaly = m.group(5)
        self.mean_motion = m.group(6)
        self.revolutions = m.group(7)

    def signal_thrusters(self):
        '''Callback function for Storm Event, may add
        functionality in the future
        '''
        pass


class Constellation():
    '''Class registering and containing all Starlink Satellites
    '''
    satellite_array = []
    num_satellites = len(satellite_array)

    def __init__(self, subscribe=None):
        self.logger = get_logger('Starlink.Constellation')
        self.logger.info('Initializing constellation')
        subscribe.magnetosphere.subscribe(self.broadcast_alert)

    def build(self):
        '''Fetches and parses Satellites from Celestrack
        and stors in satellite_array
        '''
        tle = TLEData()
        self.satellite_array = tle.fetch(STARLINK_URL)
        self.num_satellites = len(self.satellite_array)
        self.logger.info(f'Constellation assembled, {self.num_satellites} total satellites')

    def _get_vulnerable_satellites(self):
        #todo get all between sun and solar storm
        pass

    def broadcast_alert(self, e):
        '''Callback function that logs a warning to
        all satellites that a Storm Event has occurred'''
        # sat_array = self._get_vulnerable_satellites()
        for sat in self.satellite_array:
            if sat != None: #todo fix
                sat.signal_thrusters()
        self.logger.info(f'{self.num_satellites} satellite(s) have been alerted to ready their thrusters')



