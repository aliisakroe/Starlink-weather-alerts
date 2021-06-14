import abc
import requests

class API(abc.ABC):

    def fetch(self, url):
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
        pass
