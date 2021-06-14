'''This uses real-time apis from NOAA...'''

import requests
from Starlink import get_logger


class Magnetosphere():

    def __init__(self):
        self.logger = get_logger('NOAA.Magnetosphere')
        self.fetch()

    def _fetch_magnetosphere(self, url='https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json'):
        self.logger.info('Fetching Magnetosphere data from NOAA')
        try:
            r = requests.get(url)
            assert r.status_code == 200
            self.logger.info("Magnetosphere fetch successful")
        except Exception:  # todo
            raise Exception
        return self._parse(r.json())


    def _parse(self, data): #todo do I need to parse it all?
        for l in reversed(data): #get most recent first
            time_tag = l[0]
            bx_gsm = l[1]
            by_gsm = l[2]
            bz_gsm = l[3]
            lon_gsm = l[4]
            lat_gsm = l[5]
            bt = l[6]
            yield l



class Plasma():

    def __init__(self):
        self.logger = get_logger('NOAA.Plasma')
        self.fetch()

    async def _fetch_plasma(self, url='https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json'):
        self.logger.info('Fetching Plasma data from NOAA')
        try:
            r = requests.get(url)
            assert r.status_code == 200
            self.logger.info("Plasma fetch successful")
        except Exception:  # todo
            raise Exception

class SpaceWeather(Plasma, Magnetosphere):
    def __init__(self):
        self.logger = get_logger('NOAA.SpaceWeather')
        # print(list(self.fetch_magnetosphere()))


    async def fetch_plasma(self):
        await self._fetch_plasma()

    async def fetch_magnetosphere(self):
        self._fetch_magnetosphere()
