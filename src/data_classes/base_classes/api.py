''' 3 classes: Starlink TLEData, NOAA MagnetosphereData and NOAA PlasmaData implement API'''

import abc
import requests

class API(abc.ABC):
    '''Abstract class for fetching from url enpoint,
    must define how to parse the data
    '''

    def fetch(self, url):
        '''GET request from url and returns _parse(data)

        :parameter: url: str
        '''
        #todo assert url a valid url str
        try:
            r = requests.get(url)
            assert r.status_code == 200

        except requests.exceptions.HTTPError as errh:
            self.logger.error(errh)
        except requests.exceptions.ConnectionError as errc:
            self.logger.error(errc)
        except requests.exceptions.Timeout as errt:
            self.logger.error(errt)
        except requests.exceptions.RequestException as err:
            self.logger.error(err)

        return self._parse(r)

    @abc.abstractmethod
    def _parse(self, data):
        '''Absctract class cannot be instantiated
        without overriding means of parsing fetched data

        :parameter: data:Request (from fetch) can call data.text or data.json
        '''
        pass
