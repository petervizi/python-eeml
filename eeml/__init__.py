from datetime import date
from xml.dom.minidom import *

__authors__ = "Peter Vizi"
__license__ = "GPLv3"
__version__ = "0.1"
__docformat__ = "restructuredtext en"
__doc__ = """
This package provides support for handling eeml_ files in python.

Reference
=========

Almasretes.
"""

class EEML:
    """
    A class representing an EEML document.
    """

    def __init__(self):
        """
        Create a new EEML document.
        """
        self._environments = [] #: the environments in this EEML document

    def toeeml(self):
        """
        Convert this document into an EEML file.

        :return: the EEML document
        :rtype: `Document`
        """
        doc = Document()
        eeml = doc.createElement('eeml')
        eeml.setAttribute('xmlns', 'http://www.eeml.org/xsd/005')
        eeml.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        eeml.setAttribute('xsi:schemaLocation', 'http://www.eeml.org/xsd/005 http://www.eeml.org/xsd/005/005.xsd')
        eeml.setAttribute('version', '5')
        doc.appendChild(eeml)
        for env in self._environments:
            tmp = env.toeeml()
            eeml.appendChild(tmp)
        return doc

    def addEnvironment(self, env):
        """
        Add a new Environment
        
        :param env: add an `Environment` to this EEML document
        :type env: `Environment`
        """
        if isinstance(env, Environment):
            self._environments.append(env)
        else:
            raise Exception()

class Environment:
    """
    The Environment element of the document.
    """

    def __init__(self, title=None, feed=None, status=None, description=None,
                 icon=None, website=None, email=None, updated=None, creator=None, id=None):
        """
        Create a new `Environment`.

        :param title: the title
        :type title: `str`
        :param feed: the url to this `Environment`'s feed
        :type feed: `str`
        :param status: the status, valid values: ``frozen``, ``live``
        :type status: `str`
        :param description: a descriptive text
        :type description: `str`
        :param icon: an url to an icon
        :type icon: `str`
        :param website: the url to a website
        :type website: `str`
        :param email: an email address
        :type email: `str`
        :param updated: the time of update
        :type updated: `datetime.date`
        :param creator: the name of the creator
        :type creator: `str`
        :param id: en identifier
        :type id: `int`
        """
        self._title = title
        self._feed = feed
        if status not in ['frozen', 'live']:
            raise Exception()
        self._status = status
        self._description = description
        self._icon = icon
        self._website = website
        self._email = email
        self._updated = updated
        self._creator = creator
        if id:
            if int(id) < 0:
                raise Exception()
        self._id = id
        self._location = None
        self._data = []

    def setLocation(self, location):
        """
        Set the location of this `Environment`.

        :param location: the `Location`
        :type location: `Location`
        """
        if isinstance(location, Location):
            self._location = location
        else:
            raise Exception

    def addData(self, data):
        """
        Add some data to this `Environment`.

        :param data: the data to be added
        :type data: `list`, `Data`
        """
        if isinstance(data, Data):
            self._data.append(data)
        elif isinstance(data, list):
            self._data.extend(data)
        else:
            raise Exception()

    def toeeml(self):
        """
        Convert this file into eeml format.

        :return: the top element of this `Environment`
        :rtype: `Element`
        """
        doc = Document()
        env = doc.createElement('environment')
        if self._updated:
            if isinstance(self._updated, date):
                env.setAttribute('updated', self._updated.isoformat())
            else:
                env.setAttribute('updated', self._updated)
        if self._creator:
            env.setAttribute('creator', self._creator)
        if self._id:
            env.setAttribute('id', str(self._id))
        if self._title:
            tmp = doc.createElement('title')
            tmp.appendChild(doc.createTextNode(self._title))
            env.appendChild(tmp)
        if self._feed:
            tmp = doc.createElement('feed')
            tmp.appendChild(doc.createTextNode(self._feed))
            env.appendChild(tmp)
        if self._status:
            tmp = doc.createElement('status')
            tmp.appendChild(doc.createTextNode(self._status))
            doc.appendChild(tmp)
        if self._description:
            tmp = doc.createElement('description')
            tmp.appendChild(doc.createTextNode(self._description))
            env.appendChild(tmp)
        if self._icon:
            tmp = doc.createElement('icon')
            tmp.appendChild(doc.createTextNode(self._icon))
            env.appendChild(tmp)
        if self._website:
            tmp = doc.createElement('website')
            tmp.appendChild(doc.createTextNode(self._website))
            env.appendChild(tmp)
        if self._email:
            tmp = doc.createElement('email')
            tmp.appendChild(doc.createTextNode(self._email))
            env.appendChild(tmp)
        if self._location:            
            env.appendChild(self._location.toeeml())
        for data in self._data:
            env.appendChild(data.toeeml())
        return env

class Location:
    """
    A class representing the location tag of the document.
    """
    def __init__(self, name=None, lat=None, lon=None, ele=None,
                 exposure=None, domain=None, disposition=None):
        """
        :param name: a descriptive name
        :type name: `str`
        :param lat: latitude
        :type lat: `float`
        :param lon: longitude
        :type lon: `float`
        :param ele: elevation
        :type ele: `float`
        :param exposure: exposure (``indoor`` or ``outdoor``)
        :type exposure: `str`
        :param domain: domain (``physical`` or ``virtual``)
        :type domain: `str`
        :param disposition: disposition (``fixed`` or ``mobile``)
        :type disposition: `str`
        """

        self._name = name
        self._lat = lat
        self._lon = lon
        self._ele = ele
        if exposure:
            if exposure in ['indoor', 'outdoor']:
                self._exposure = exposure
            else:
                raise Exception()
        if domain:
            if domain in ['physical', 'virtual']:
                self._domain = domain
            else:
                raise Exception()
        else:
            raise Exception()
        if disposition:
            if disposition in ['fixed', 'mobile']:
                self._disposition = disposition
            else:
                raise Exception()

    def toeeml(self):
        """
        Convert this class into a EEML DOM element.

        :return: the location element
        :rtype: `Element`
        """

        doc = Document()
        loc = doc.createElement('location')
        if self._exposure:
            loc.setAttribute('exposure', self._exposure)
        if self._domain:
            loc.setAttribute('domain', self._domain)
        if self._disposition:
            loc.setAttribute('disposition', self._disposition)
        if self._name:
            tmp = doc.createElement('name')
            tmp.appendChild(doc.createTextNode(self._name))
            loc.appendChild(tmp)
        if self._lat:
            tmp = doc.createElement('lat')
            tmp.appendChild(doc.createTextNode(str(self._lat)))
            loc.appendChild(tmp)
        if self._lon:
            tmp = doc.createElement('lon')
            tmp.appendChild(doc.createTextNode(str(self._lon)))
            loc.appendChild(tmp)
        if self._ele:
            tmp = doc.createElement('ele')
            tmp.appendChild(doc.createTextNode(str(self._ele)))
            loc.appendChild(tmp)

        return loc

class Data:
    """
    The Data element of the document
    """

    def __init__(self, id, value, tags=[], minValue=None, maxValue=None, unit=None):
        """
        Create a new Data

        :param id: the identifier of this data
        :type id: `int`
        :param value: the value of the data
        :type value: `float`
        :param tags: the tags on this data
        :type tags: `list`
        :param maxValue: the maximum value of this data
        :type maxValue: `float`
        :param minValue: the minimum value of this data
        :type minValue: `float`
        :param unit: a `Unit` for this data
        :type unit: `Unit`
        """
        self._id = id        
        self._value = value
        self._tags = tags
        
        self._minValue = minValue
        self._maxValue = maxValue
        if unit:
            if not isinstance(unit, Unit):
                raise Exception()
        self._unit = unit

    def toeeml(self):
        """
        Convert this element into a DOM object.

        :return: a data element
        :rtype: `Element`
        """

        doc = Document()
        data = doc.createElement('data')
        data.setAttribute('id', str(self._id))
        for tag in self._tags:
            tmp = doc.createElement('tag')
            tmp.appendChild(doc.createTextNode(tag))
            data.appendChild(tmp)
        tmp = doc.createElement('value')
        if self._minValue:
            tmp.setAttribute('minValue', str(self._minValue))
        if self._minValue:
            tmp.setAttribute('maxValue', str(self._maxValue))
        tmp.appendChild(doc.createTextNode(str(self._value)))
        data.appendChild(tmp)
        if self._unit:
            data.appendChild(self._unit.toeeml())
        return data

class Unit:
    """
    This class represents a unit element in the EEML document.
    """

    def __init__(self, name, type=None, symbol=None):
        """
        :param name: the name of this unit (eg. meter, Celsius)
        :type name: `str`
        :param type: the type of this unit (``basicSI``, ``derivedSI``, ``conversionBasedUnits``, ``derivedUnits``, ``contextDependentUnits``)
        :type type: `str`
        :param symbol: the symbol of this unit (eg. m, C)
        :type symbol: `str`
        """

        self._name = name
        if type:
            if type in ['basicSI', 'derivedSI', 'conversionBasedUnits', 'derivedUnits', 'contextDependentUnits']:
                self._type = type
            else:
                raise Exception()
        self._type = type
        self._symbol = symbol

    def toeeml(self):
        """
        Convert this object into a DOM element.

        :return: the unit element
        :rtype: `Element`
        """

        doc = Document()
        unit = doc.createElement('unit')
        if self._type:
            unit.setAttribute('type', self._type)
        if self._symbol:
            unit.setAttribute('symbol', self._symbol)

        unit.appendChild(doc.createTextNode(self._name))
        return unit

def create_eeml(env, loc, data):
    """
    Create an `EEML` document from the parameters.

    :param env: the environment
    :type env: `Environment`
    :param loc: the location
    :type loc: `Location`
    :param data: the data
    :type data: `list`, `Data`
    """
    eeml = EEML()
    env.setLocation(loc)
    eeml.addEnvironment(env)
    env.addData(data)
    return eeml
