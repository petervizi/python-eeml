import eeml
import httplib
import re

__authors__ = "Peter Vizi"
__license__ = "GPLv3"
__version__ = "0.1"
__docformat__ = "restructuredtext en"
__doc__ = """
The way to handle data streams, and put it to the pachube server.
"""

url_pattern = re.compile("/v[12]/feeds/\d+\.xml")

class Pachube(object):
    """
    A class for manually updating a pachube data stream.
    """

    def __init__(self, url, key):
        """
        :param url: the api url either '/v2/feeds/1275.xml' or 1275
        :type url: `str`
        :param key: your personal api key
        :type key: `str`
        """
        if str(url) == url:
            if(url_pattern.match(url)):
                self._url = url
            else:
                raise ValueError("The url argument has to be in the form '/v2/feeds/1275.xml' or 1275")
        else:
            try:
                if int(url) == url:
                    self._url = '/v2/feeds/' + str(url) + '.xml'
                else:
                    raise TypeError('')
            except TypeError:
                raise TypeError("The url argument has to be in the form '/v2/feeds/1275.xml' or 1275")
        self._key = key
        self._eeml = eeml.create_eeml(eeml.Environment(), None, [])

    def update(self, data):
        """
        Update a data stream.

        :param data: the data to be updated
        :type data: `Data`, `list`
        """
        self._eeml.updateData(data)

    def put(self):
        """
        Put the information to the website.

        :raise Exception: if there was problem with the communication
        """
        conn = httplib.HTTPConnection('api.pachube.com:80')
        conn.request('PUT', self._url, self._eeml.toeeml().toxml(), {'X-PachubeApiKey': self._key})
        resp = conn.getresponse()
        if resp.status != 200:
            raise Exception(resp.reason)
        resp.read()
        conn.close()
