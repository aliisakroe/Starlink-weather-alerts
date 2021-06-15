'''Uses Real-Time Space Weather Data from NOAA website. Magnetosphere will indicate when storms make LEO satellites
vulnerable, and the Plasma radiation will indicate the intensity of the storm
'''

from src.data_classes.base_classes.api import API
from src.data_classes.base_classes.database import Database
from src.data_classes.base_classes.observer import Observable, Event
from src.utils.logging import get_logger

MAGNETOSPHERE_URL='https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json'
PLASMA_URL='https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json'
DB='NOAA'

def _get_hourly(timestamp):
    '''Helper function to only log 1 unique storm every hour'''
    #todo better way of doing this
    return timestamp[:-10]

class Storm(Event):
    '''Event class used to trigger callbacks
    May be extended in the future to utilize Plasma Data parameters'''
    def __init__(self, args):
        self.time_tag, self.bx_gsm, self.by_gsm, self.bz_gsm, self.lon_gsm, self.lat_gsm, self.bt = args

class MagnetosphereDB(Database):
    '''STORMS table in NOAA to store unique storm every hour'''
    logger = get_logger('NOAA.StormDB')

    def create_table(self):
        '''Stores all data retrieved from API endpoint
        though only bz_gsm is used
        '''
        with self.con as con:
            con.execute(f"""
                               CREATE TABLE IF NOT EXISTS {self.name} (
                                time_tag TEXT PRIMARY KEY, 
                                   bx_gsm float, 
                                   by_gsm float, 
                                   bz_gsm float, 
                                   lon_gsm float, 
                                   lat_gsm float, 
                                   bt float
                               );
                           """)

        self.logger.info('StormDB table created')

    def write_many_rows(self, storm):
        ''''Insert only unique hourly rows
        '''
        sql = f'INSERT OR IGNORE INTO {self.name} (time_tag, bx_gsm, by_gsm, bz_gsm, lon_gsm, lat_gsm, bt) values(?, ?, ?, ?, ?, ?, ?);'
        with self.con as con:
            con.execute(sql, storm).fetchmany()

class MagnetosphereData(API, Observable):
    '''Fetches weather from Magnetosphere API endpoint and
    classifies and stores storms in MagnetosphereDB and
    registers storms to trigger callbacks'''
    logger = get_logger('NOAA.Magnetosphere')

    def __init__(self):
        self.callbacks = []
        self.db = MagnetosphereDB(db=DB, table='STORMS')
        self.db.create_table()

    def possible_storm(self, bz_gsm):
        '''Classifying storm

        :parameter: bz_gsm: Float

        If negative, the magnetosphere is peeling Southward
        '''
        if bz_gsm != 'bz_gsm' and float(bz_gsm) < 0:
            return True

    def _parse(self, data):
        '''Parses Request data into json and stores values into STORMS Table

        :parameter: data: Request

        '''
        count = 0
        for i, l in enumerate(data.json()[1:]):
            time_tag = _get_hourly(l[0])
            bx_gsm = l[1]
            by_gsm = l[2]
            bz_gsm = l[3]
            lon_gsm = l[4]
            lat_gsm = l[5]
            bt = l[6]
            if self.possible_storm(bz_gsm):
                count+=1
                self.db.write_many_rows((time_tag, bx_gsm, by_gsm, bz_gsm, lon_gsm, lat_gsm, bt))

        self.logger.info(f'wrote {self.db.get_num_rows()} unique timestamp / {count} rows to {self.db.name}')



    def check_for_storms(self):
        '''Only storms are written to STORMS table, so return all rows
        Table will be cleared with each subsequent fetch
        '''
        storms = self.db.execute(f"SELECT * FROM {self.db.name};")
        self.logger.info(f'retrieved {len(storms)} storms from the database')
        for s in storms:
            (time_tag, bx_gsm, by_gsm, bz_gsm, lon_gsm, lat_gsm, bt) = s
            self.fire(Storm, time_tag=time_tag, bx_gsm=bx_gsm, by_gsm=by_gsm, bz_gsm=bz_gsm, lon_gsm=lon_gsm, lat_gsm=lat_gsm, bt=bt)


class PlasmaDB(Database):
    '''PLASMA table in NOAA to store unique storm every hour'''
    logger = get_logger('NOAA.PlasmaDB')

    def create_table(self):
        '''Stores all data retrieved from API endpoint
        for future research
        '''
        with self.con:
            self.con.execute(f"""
                                  CREATE TABLE IF NOT EXISTS {self.name} (
                                      time_tag TEXT UNIQUE,
                                      density FLOAT,
                                      speed FLOAT,
                                      temperature INTEGER 
                                  );
                              """)

        self.logger.info('PlasmaDB table created')

    def write_many_rows(self, data):
        ''''Insert only unique hourly rows
                '''
        self.logger.info('Writing Drag to database for storm lookups')
        sql = f'INSERT OR IGNORE INTO {self.name} (time_tag, density, speed, temperature) values(?, ?, ?, ?)'
        with self.con:
            self.con.executemany(sql, data)
        self.logger.info('Storm lookups written successfully')

class PlasmaData(API):
    '''Fetches weather from Plasma API endpoint and
        classifies and stores in PlasmaDB
        '''
    def __init__(self, magnetosphere):
        self.logger = get_logger('NOAA.Plasma')
        self.db = PlasmaDB(db='NOAA', table='PLASMA')
        self.db.create_table()

        magnetosphere.subscribe(self.get_radiation_drag)

    def _parse(self, data):
        '''Parses Request data into json and stores values into STORMS Table

        :parameter: data: Request

        '''
        text = data.json()[1:]
        data1 = [[_get_hourly(l[0])] + l[1:] for l in text]
        data = [tuple(l) for l in data1]

        self.db.write_many_rows(data)

        self.logger.info(f'wrote {self.db.get_num_rows()} unique timestamp / {len(data)} rows to {self.db.name}')

    def get_radiation_drag(self, e):
        '''Callback to log plasma intensity data
        for each hourly storm
        '''
        #todo get the right drag for the time
        hourly_storm_time = e.time_tag[1]
        rows = self.db.execute(f'SELECT * FROM {self.db.name} WHERE time_tag = "{hourly_storm_time}"')

        for row in rows:
            self.logger.warn(f'At {row[0]} there has been a {row[1]} density {row[2]} speed and {row[3]} temperature storm')

class SpaceWeather(object):
    '''Orchestration class to call Magnetosphere and Plasma APIs
    and search for storms
    '''
    magnetosphere = MagnetosphereData()

    def __init__(self):
        self.logger = get_logger('NOAA.SpaceWeather')
        self.logger.info('Gathering Plasma and Magnetosphere for Space Weather')
        self.plasma = PlasmaData(self.magnetosphere)

    async def fetch_plasma(self):
        '''Coroutine for logging Plasma data
        '''
        self.logger.info("Kicking off plasma"),
        try:
            self.plasma.fetch(PLASMA_URL)
        except Exception as err:
            err

    async def fetch_magnetosphere(self):
        '''Coroutine for logging Storms from Magnetosphere Data
        '''
        self.logger.info("Kicking off magnetosphere"),
        try:
            self.magnetosphere.fetch(MAGNETOSPHERE_URL)
        except Exception as err:
            err


    async def run_weather(self):
        '''Coroutine for triggering storm event callbacks such as
        logging plasma intensity and signalling satellite thrusters
        '''
        self.logger.info("Checking space weather for storms")
        self.magnetosphere.check_for_storms()




