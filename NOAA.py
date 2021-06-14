'''This uses real-time apis from NOAA...'''

import requests
import sqlite3 as sl
from Starlink import get_logger

class Storm():
    def __init__(self, args):
        self.time_tag, self.bx_gsm, self.by_gsm, self.bz_gsm, self.lon_gsm, self.lat_gsm, self.bt = args

class Observable(object):
    def __init__(self):
        self.callbacks = []
        self.logger = get_logger('NOAA.Observable')

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def fire(self, **attrs):
        e = Storm(attrs.items())
        self.logger.info("A storm is present, preparing starlinks")
        e.source = self
        for fn in self.callbacks:
            fn(e)

class Magnetosphere(Observable):

    def __init__(self):
        self.callbacks = []
        self.logger = get_logger('NOAA.Magnetosphere')
        # self.fetch()

    def update_data(self, url='https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json'):
        self.logger.info('Fetching Magnetosphere data from NOAA')
        try:
            r = requests.get(url)

        except requests.exceptions.HTTPError as errh:
            self.logger.error(errh)
        except requests.exceptions.ConnectionError as errc:
            self.logger.error(errc)
        except requests.exceptions.Timeout as errt:
            self.logger.error(errt)
        except requests.exceptions.RequestException as err:
            self.logger.error(err)

        assert r.status_code == 200
        self.logger.info("Magnetosphere fetch successful")

        return self._parse(r.json())

    def _parse(self, data): #todo do I need tos parse it all?
        for l in reversed(data): #get most recent first
            time_tag = l[0]
            bx_gsm = l[1]
            by_gsm = l[2]
            bz_gsm = l[3]
            lon_gsm = l[4]
            lat_gsm = l[5]
            bt = l[6]
            if float(bz_gsm) < 0:
                self.logger.warn(f'Magnetic STORM Alert, {bz_gsm}')
                self.fire(time_tag=time_tag, bx_gsm=bx_gsm, by_gsm=by_gsm, bz_gsm=bz_gsm, lon_gsm=lon_gsm, lat_gsm=lat_gsm, bt=bt)
            return l

class Plasma():

    def __aenter__(self):
        return self.con

    def __init__(self, magnetosphere):
        self.logger = get_logger('NOAA.Plasma')
        self.open_connection()
        # text = self.fetch()
        # self.store_data(text)
        magnetosphere.subscribe(self.get_radiation_drag)

    def update_data(self, url='https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json'):
        self.logger.info('Fetching Plasma data from NOAA')
        try:
            r = requests.get(url)
        except requests.exceptions.HTTPError as errh:
            self.logger.error(errh)
        except requests.exceptions.ConnectionError as errc:
            self.logger.error(errc)
        except requests.exceptions.Timeout as errt:
            self.logger.error(errt)
        except requests.exceptions.RequestException as err:
            self.logger.error(err)

        assert r.status_code == 200
        self.logger.info("Plasma fetch successful")

        text = r.json()

        self.store_data(text)


    def open_connection(self):
        self.con = sl.connect('drag.db')
        with self.con:
            self.con.execute("""
                               CREATE TABLE IF NOT EXISTS DRAG (
                                   time_tag substring ,
                                   density FLOAT,
                                   speed FLOAT,
                                   temperature INTEGER 
                               );
                           """)

    def store_data(self, data):
        self.logger.info('Writing to database')
        all_data = [tuple(l) for l in data]
        sql = 'INSERT INTO DRAG (time_tag, density, speed, temperature) values(?, ?, ?, ?)'
        with self.con:
            self.con.executemany(sql, all_data)

    # def __aexit__(self, exc_type, exc, tb):
    #     self.con.close()

    def get_radiation_drag(self, e):
        #todo get the right drag for the time
        storm_time = e.time_tag[1]
        with self.con:
            data = self.con.execute(f"SELECT * FROM DRAG WHERE time_tag = '{storm_time}'")
            for row in data:
                self.logger.warn(f'At {row[0]} there has been a {row[1]} density {row[2]} speed and {row[3]} temperature storm')

class SpaceWeather():

    magnetosphere = Magnetosphere()

    def __init__(self):
        self.logger = get_logger('NOAA.SpaceWeather')
        self.logger.info('Gathering Plasma and Magnetosphere for Space Weather')
        self.plasma = Plasma(self.magnetosphere)

    async def fetch_plasma(self):
        self.plasma.update_data()

    async def fetch_magnetosphere(self):
        self.magnetosphere.update_data()




