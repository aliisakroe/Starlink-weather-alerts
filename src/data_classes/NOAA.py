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

class StormDB():
    def __init__(self):
        self.logger = get_logger("NOAA.StormDB")
        self.open_connection()

    def open_connection(self):
        self.con = sl.connect('NOAA.db')
        with self.con:
            self.con.execute("""
                               CREATE TABLE IF NOT EXISTS STORMS (
                                    time_tag substring UNIQUE, 
                                   bx_gsm float, 
                                   by_gsm float, 
                                   bz_gsm float, 
                                   lon_gsm float, 
                                   lat_gsm float, 
                                   bt float
                               );
                           """)

    def __aenter__(self):
        return self.con.cursor()

    def store_data(self, storm):
        sql = 'INSERT OR IGNORE INTO STORMS (time_tag, bx_gsm, by_gsm, bz_gsm, lon_gsm, lat_gsm, bt) values(?, ?, ?, ?, ?, ?, ?);'
        with self.con as con:
            con.execute(sql, storm)

    def __aexit__(self, exc_type, exc, tb):
        with self.con:
            self.con.close()

class MagnetosphereData(Observable):

    def __init__(self):
        self.callbacks = []
        self.logger = get_logger('NOAA.Magnetosphere')
        # self.fetch()
        self.db = StormDB()

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
            if bz_gsm != 'bz_gsm' and float(bz_gsm) < 0:
                self.db.store_data((time_tag, bx_gsm, by_gsm, bz_gsm, lon_gsm, lat_gsm, bt))

    def check_for_storms(self):
        self.logger.info('Checking for storms')

        with self.db.con as con:
            storms = con.execute("SELECT * FROM STORMS;").fetchall()
            # print(storms)

        self.logger.warn(f'Magnetic STORM Alert')

        for storm in storms:
            (time_tag, bx_gsm, by_gsm, bz_gsm, lon_gsm, lat_gsm, bt) = storm
            self.fire(time_tag=time_tag, bx_gsm=bx_gsm, by_gsm=by_gsm, bz_gsm=bz_gsm, lon_gsm=lon_gsm, lat_gsm=lat_gsm, bt=bt)



class PlasmaDB():
    def __aenter__(self):
        return self.con

    def __init__(self):
        self.logger = get_logger('NOAA.PlasmaDB')
        self.open_connection()

    def open_connection(self):
        self.con = sl.connect('NOAA.db')
        with self.con:
            self.con.execute("""
                                  CREATE TABLE IF NOT EXISTS DRAG (
                                      time_tag substring UNIQUE,
                                      density FLOAT,
                                      speed FLOAT,
                                      temperature INTEGER 
                                  );
                              """)
            self.con.execute('delete from drag').fetchone() #todo hacky
            print(self.con.execute('select count(*) from drag').fetchone())

    def store_data(self, data):
        self.logger.info('Writing Drag to database for storm lookups')
        all_data = [tuple(l) for l in data]
        sql = 'INSERT INTO DRAG (time_tag, density, speed, temperature) values(?, ?, ?, ?)'
        with self.con:
            self.con.executemany(sql, all_data)

    def __aexit__(self, exc_type, exc, tb):
        if exc_type == KeyboardInterrupt:
            with self.con:
                self.con.execute("DELETE FROM DRAG;")
                print(self.con.execute('select count(*) from drag;'))
                self.con.close()


class Plasma():

    def __init__(self, magnetosphere):
        self.logger = get_logger('NOAA.Plasma')
        self.db = PlasmaDB()
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

        self.db.store_data(text)


    def get_radiation_drag(self, e):
        #todo get the right drag for the time
        storm_time = e.time_tag[1]
        with self.db.con as con:
            data = con.execute(f"SELECT * FROM DRAG WHERE time_tag = '{storm_time}'").fetchall()
            # print(data)
            for row in data:
                self.logger.warn(f'At {row[0]} there has been a {row[1]} density {row[2]} speed and {row[3]} temperature storm')

class SpaceWeather():

    magnetosphere = MagnetosphereData()

    def __init__(self):
        self.logger = get_logger('NOAA.SpaceWeather')
        self.logger.info('Gathering Plasma and Magnetosphere for Space Weather')
        self.plasma = Plasma(self.magnetosphere)

    async def fetch_plasma(self):
        self.plasma.update_data()

    async def fetch_magnetosphere(self):
        self.magnetosphere.update_data()

    def run_weather(self):
        self.magnetosphere.check_for_storms()




