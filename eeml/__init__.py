# -*- coding: utf-8 -*-

from datetime import date, datetime

try:
    from lxml import etree
except ImportError: # If lxml is not there try python standard lib
    from xml.etree import ElementTree as etree

from datastream import *

__authors__ = "Peter Vizi"
__license__ = "GPLv3"
__docformat__ = "restructuredtext en"
__doc__ = """
This package provides support for handling eeml files in python.

Usage
=====

Look at the test directory.
"""

EEML_NAMESPACE = 'http://www.eeml.org/xsd/0.5.1'
XSI_NAMESPACE = 'http://www.w3.org/2001/XMLSchema-instance'
NSMAP = {None: EEML_NAMESPACE,
         'xsi': XSI_NAMESPACE}

def _elem(name):
    return etree.Element("{%s}%s" % (EEML_NAMESPACE, name), nsmap=NSMAP)

class Environment(object):
    """
    The Environment element of the document.
    """

    def __init__(self, title=None, feed=None, status=None, description=None,
                 icon=None, website=None, email=None, updated=None, creator=None, id_=None, private=None):
        """
        Create a new `Environment`.

        :raise Exception: if sg is wrong

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
        :param id_: an identifier
        :type id_: `int`
        """
        self._title = title
        self._feed = feed
        if status and status not in ['frozen', 'live']:
                raise ValueError("status must be either 'frozen' or 'live', got %s" % status)
        self._status = status
        self._description = description
        self._icon = icon
        self._website = website
        self._email = email
        self._updated = updated
        self._creator = creator
        if id_ and int(id_) < 0:
            raise ValueError("id must be a positive integer")
        self._id = id_
        self._location = None
        self._data = {}
        self._private = private

    def setLocation(self, location):
        """
        Set the location of this `Environment`.

        :raise Exception: if `location` is not `Location` type

        :param location: the `Location`
        :type location: `Location`
        """
        if isinstance(location, Location):
            self._location = location
        else:
            raise ValueError("location must be a Location object, got %s" % type(location))

    def updateData(self, data):
        if isinstance(data, Data):
            self._data[data.id] = data
        elif isinstance(data, list):
            for d in data:
                self._data[d.id] = d

    def toeeml(self):
        """
        Convert this file into eeml format.

        :return: the top element of this `Environment`
        :rtype: `Element`
        """
        env = _elem('environment')
        if self._updated:
            if isinstance(self._updated, (date, datetime,)):
                env.attrib['updated'] =  self._updated.isoformat()
            else:
                env.attrib['updated'] = self._updated
        if self._creator:
            env.attrib['creator'] = self._creator
        if self._id:
            env.attrib['id'] = str(self._id)
        if self._title:
            tmp = _elem('title')
            tmp.text = self._title
            env.append(tmp)
        if self._feed:
            tmp = _elem('feed')
            tmp.text = self._feed
            env.append(tmp)
        if self._status:
            tmp = _elem('status')
            tmp.text = self._status
            env.append(tmp)
        if self._description:
            tmp = _elem('description')
            tmp.text = self._description
            env.append(tmp)
        if self._icon:
            tmp = _elem('icon')
            tmp.text = self._icon
            env.append(tmp)
        if self._website:
            tmp = _elem('website')
            tmp.text = self._website
            env.append(tmp)
        if self._email:
            tmp = _elem('email')
            tmp.text = self._email
            env.append(tmp)
        if self._private is not None:
            tmp = _elem('private')
            tmp.text = str(self._private).lower()
            env.append(tmp)
        if self._location:            
            env.append(self._location.toeeml())
        for data in self._data.itervalues():
            env.append(data.toeeml())
        return env


class EEML(object):
    """
    A class representing an EEML document.
    """

    def __init__(self, environment=Environment()):
        """
        Create a new EEML document.
        """
        self._environment = environment #: the environments in this EEML document

    def toeeml(self):
        """
        Convert this document into an EEML file.

        :return: the EEML document
        :rtype: `Document`
        """
        eeml = _elem('eeml')

        eeml.attrib['{%s}schemaLocation' % XSI_NAMESPACE] = 'http://www.eeml.org/xsd/0.5.1 http://www.eeml.org/xsd/0.5.1/0.5.1.xsd'
        eeml.attrib['version'] = '0.5.1'

        eeml.append(self._environment.toeeml())

        return eeml

    def setEnvironment(self, env):
        """
        Add a new Environment

        :raise Exception: if `env` is not an `Environment`
        
        :param env: add an `Environment` to this EEML document
        :type env: `Environment`
        """
        if isinstance(env, Environment):
            self._environment = env
        else:
            raise ValueError("env must be an Environment object, got %s" % type(env))

    def updateData(self, data):
        """
        Update a data value.

        :param data: the new data
        :type data: `Data`, `list`
        """

        if not self._environment: 
            raise Exception("Environment not set, cannot update data.")
        self._environment.updateData(data)


class Location(object):
    """
    A class representing the location tag of the document.
    """
    def __init__(self, name=None, lat=None, lon=None, ele=None,
                 exposure=None, domain=None, disposition=None):
        """
        :raise Exception: if sg is wrong

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

        if exposure and exposure not in ['indoor', 'outdoor']:
            raise ValueError("exposure must be 'indoor' or 'outdoor', got '%s'" % exposure)
        self._exposure = exposure

        if domain and domain not in ['physical', 'virtual']:
            raise ValueError("domain must be 'physical' or 'virtual', got '%s'" % domain)
        self._domain = domain

        if disposition and disposition not in ['fixed', 'mobile']:
            raise ValueError("disposition must be 'fixed' or 'mobile', got '%s'" % disposition)
        self._disposition = disposition

    def toeeml(self):
        """
        Convert this class into a EEML DOM element.

        :return: the location element
        :rtype: `Element`
        """

        loc = _elem('location')
        if self._exposure:
            loc.attrib['exposure'] =  self._exposure
        if self._domain:
            loc.attrib['domain'] = self._domain
        if self._disposition:
            loc.attrib['disposition'] =  self._disposition
        if self._name:
            tmp = _elem('name')
            tmp.text = self._name
            loc.append(tmp)
        if self._lat:
            tmp = _elem('lat')
            tmp.text = str(self._lat)
            loc.append(tmp)
        if self._lon:
            tmp = _elem('lon')
            tmp.text = str(self._lon)
            loc.append(tmp)
        if self._ele:
            tmp = _elem('ele')
            tmp.text = str(self._ele)
            loc.append(tmp)

        return loc


class Data(object):
    """
    The Data element of the document
    """

    def __init__(self, id_, value, tags=[], minValue=None, maxValue=None, unit=None, at=None):
        """
        Create a new Data

        :param id_: the identifier of this data
        :type id_: `int`
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
        self._id = id_
        self._value = value
        self._tags = tags
        
        self._minValue = minValue
        self._maxValue = maxValue
        if unit is not None and not isinstance(unit, Unit):
            raise ValueError("unit must be an instance of Unit, got %s" % type(unit))
        self._unit = unit
        if at is not None and not isinstance(at, datetime):
            raise ValueError("at must be an instance of datetime.datetime, got %s" % type(at))
        self._at = at

    def getId(self):
        return self._id

    id = property(getId)

    def toeeml(self):
        """
        Convert this element into a DOM object.

        :return: a data element
        :rtype: `Element`
        """

        data = _elem('data')
        data.attrib['id'] = str(self._id)
        for tag in self._tags:
            tmp = _elem('tag')
            tmp.text = tag
            data.append(tmp)

        tmp = _elem('current_value')
        if self._minValue is not None:
            tmp.attrib['minValue']  = str(self._minValue)
        if self._maxValue is not None:
            tmp.attrib['maxValue'] = str(self._maxValue)
        if self._at is not None:
            tmp.attrib['at'] = self._at.isoformat()
        tmp.text = str(self._value)
        data.append(tmp)

        if self._unit:
            data.append(self._unit.toeeml())

        return data


class Unit(object):
    """
    This class represents a unit element in the EEML document.
    """

    def __init__(self, name, type_=None, symbol=None):
        """
        :raise Exception: is sg is wrong

        :param name: the name of this unit (eg. meter, Celsius)
        :type name: `str`
        :param type_: the type of this unit (``basicSI``, ``derivedSI``, ``conversionBasedUnits``, ``derivedUnits``, ``contextDependentUnits``)
        :type type: `str`
        :param symbol: the symbol of this unit (eg. m, C)
        :type symbol: `str`
        """

        self._name = name
        self.__valid_types = ['basicSI', 'derivedSI', 'conversionBasedUnits', 'derivedUnits', 'contextDependentUnits']
        if type_ and type_ in self.__valid_types:
            self._type = type
        else:
            raise ValueError("type must be %s, got '%s'" % (
                ", ".join(['%s'%s for s in self.__valid_types]), type))
        self._type = type_
        self._symbol = symbol

    def toeeml(self):
        """
        Convert this object into a DOM element.

        :return: the unit element
        :rtype: `Element`
        """

        unit = _elem('unit')
        if self._type:
            unit.attrib['type'] =  self._type
        if self._symbol:
            unit.attrib['symbol'] = self._symbol

        unit.text = self._name

        return unit


class Celsius(Unit):
    """
    Degree Celsius unit class.
    """

    def __init__(self):
        """
        Initialize the `Unit` parameters with Celsius.
        """
        Unit.__init__(self, 'Celsius', 'derivedSI', u'\xb0C')


class Fahrenheit(Unit):
    """
    Degree Fahrenheit unit class.
    """

    def __init__(self):
        """
        Initialize the `Unit` parameters with Fahrenheit.
        """
        Unit.__init__(self, 'Fahrenheit', 'derivedSI', u'\xb0F')


class RH(Unit):
    """
    Relative Humidity unit class.
    """

    def __init__(self):
        """
        Initialize the `Unit` parameters with Relative Humidity.
        """
        Unit.__init__(self, 'Relative Humidity', 'derivedUnits', '%RH')


class Watt(Unit):
    """
    Watt unit class.
    """

    def __init__(self):
        """
        Initialize the `Unit` parameters with Watt.
        """
        Unit.__init__(self, 'Watt', 'derivedSI', 'W')


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
    if loc:
        env.setLocation(loc)
    eeml.setEnvironment(env)
    env.updateData(data)
    return eeml
