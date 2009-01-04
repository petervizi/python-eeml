import eeml
import httplib

__authors__ = "Peter Vizi"
__license__ = "GPLv3"
__version__ = "0.1"
__docformat__ = "restructuredtext en"
__doc__ = """
The way to handle data streams, and put it to the pachube server.
"""

class Pachube(object):
    """
    A class for manually updating a pachube data stream.
    """

    def __init__(self, url, key):
        """
        :param url: the api url (eg. '/api/1275.xml')
        :type url: `str`
        :param key: your personal api key
        :type key: `str`
        """

        self._url = url
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
        conn = httplib.HTTPConnection('www.pachube.com:80')
        conn.request('PUT', self._url, self._eeml.toeeml().toxml(), {'X-PachubeApiKey': self._key})
        resp = conn.getresponse()
        if resp.status != 200:
            raise Exception(resp.reason)
        resp.read()
        conn.close()
