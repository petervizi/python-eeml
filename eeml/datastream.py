import eeml
import httplib
import re
from lxml import etree

url_pattern = re.compile("/v[12]/feeds/\d+\.xml")

class CosmError(Exception):
    pass

class Cosm(object):
    """
    A class for manually updating a Cosm data stream.
    """

    host = 'api.cosm.com'

    def __init__(self, url, key, env=None, loc=None, dat=[], use_https=True, timeout=10):
        """
        :param url: the api url either '/v2/feeds/1275.xml' or 1275
        :type url: `str`
        :param key: your personal api key
        :type key: `str`
        """
        if not env:
            env = eeml.Environment()
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
        self._use_https = use_https
        self._eeml = eeml.create_eeml(env, loc, dat)
        self._http_timeout = timeout

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

        :raise CosmError: if there was problem with the communication
        """
        if self._use_https:
            conn = httplib.HTTPSConnection(self.host, timeout=self._http_timeout)
        else:
            conn = httplib.HTTPConnection(self.host, timeout=self._http_timeout)

        conn.request('PUT', self._url, self.geteeml(False), {'X-ApiKey': self._key})
        conn.sock.settimeout(5.0)
        resp = conn.getresponse()
        if resp.status != 200:
            try:
                errors = etree.fromstring(resp.read())
                msg = "%s: %s" % (errors[0].text, errors[1].text)
            except:
                msg = resp.reason
            raise CosmError(msg)
        resp.read()
        conn.close()

    def geteeml(self, pretty_print=True):
        return etree.tostring(self._eeml.toeeml(), encoding='UTF-8', pretty_print=pretty_print)

class Pachube(Cosm):
    """
    For backward compatibility
    """
    pass
