# -*- coding: utf-8 -*-
"""
This package provides support for handling eeml files in python.

Usage
=====

Look at the test directory.
"""

__authors__ = "Peter Vizi"
__license__ = "GPLv3"
__docformat__ = "restructuredtext en"

from datetime import date, datetime

from eeml.namespace import EEML_SCHEMA_VERSION, SCHEMA_LOCATION
from eeml.unit import Unit
from eeml.util import _elem, _addE, _addA, _assertPosInt

class Environment(object):
    """
    The Environment element of the document.
    """

    def __init__(self, title=None, feed=None, status=None, description=None,
                 icon=None, website=None, email=None, updated=None,
                 creator=None, id_=None, private=None):
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
            raise ValueError("status must be either 'frozen' or 'live', "
                             "got {}".format(status))
        self._status = status
        self._description = description
        self._icon = icon
        self._website = website
        self._email = email
        self._updated = updated
        self._creator = creator
        _assertPosInt(id_, 'id', False)
        self._id = id_
        self._location = None
        self._data = []
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
            raise ValueError("location must be a Location object, got {}"
                             .format(type(location)))

    def updateData(self, data):
        """
        Update data

        :param data: the data to add
        :type data: `Data`, list of `Data` or `DataPoints` object
        """
        if isinstance(data, Data):
            self._data.append(data)
        elif isinstance(data, DataPoints):
            for oldData in self._data:
                if oldData._id == data._id:
                    oldData._datapoints = data
                    return
            self._data.append(Data(data._id, None, datapoints=data))
        elif isinstance(data, list):
            for dat in data:
                self._data.append(dat)

    def toeeml(self):
        """
        Convert this file into eeml format.

        :return: the top element of this `Environment`
        :rtype: `Element`
        """
        env = _elem('environment')
        if isinstance(self._updated, (date, datetime,)):
            _addA(env, self._updated, 'updated', lambda x: x.isoformat())
        elif self._updated is not None:
            _addA(env, self._updated, 'updated')
        _addA(env, self._creator, 'creator')
        _addA(env, self._id, 'id', str)
        _addE(env, self._title, 'title')
        _addE(env, self._feed, 'feed')
        _addE(env, self._status, 'status')
        _addE(env, self._description, 'description')
        _addE(env, self._icon, 'icon')
        _addE(env, self._website, 'website')
        _addE(env, self._email, 'email')
        _addE(env, self._private, 'private')
        if self._location is not None:
            env.append(self._location.toeeml())
        for data in self._data:
            env.append(data.toeeml())
        return env


class EEML(object):
    """
    A class representing an EEML document.
    """

    def __init__(self, environment=Environment()):
        """
        Create a new EEML document.

        :param environment: the environment in this EEML document
        :type environment: `Environemnt`
        """
        self._environment = None
        self.setEnvironment(environment)

    def toeeml(self):
        """
        Convert this document into an EEML file.

        :return: the EEML document
        :rtype: `Document`
        """
        eeml = _elem('eeml')

        eeml.attrib[SCHEMA_LOCATION[0]] = SCHEMA_LOCATION[1]    
        eeml.attrib['version'] = EEML_SCHEMA_VERSION

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
            raise ValueError("env must be an Environment object, got {}"
                             .format(type(env)))

    def updateData(self, data):
        """
        Update a data value.

        :param data: the new data
        :type data: `Data`, `list`
        """

        if self._environment is None:
            raise Exception("Environment not set, cannot update data.")
        self._environment.updateData(data)


class Location(object):
    """
    A class representing the location tag of the document.
    """
    def __init__(self, domain, name=None, lat=None, lon=None, ele=None,
                 exposure=None, disposition=None):
        """
        :raise Exception: if sg is wrong

        :param domain: domain (``physical`` or ``virtual``)
        :type domain: `str`
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
        :param disposition: disposition (``fixed`` or ``mobile``)
        :type disposition: `str`
        """

        self._name = name
        self._lat = lat
        self._lon = lon
        self._ele = ele

        if exposure is not None and exposure not in ['indoor', 'outdoor']:
            raise ValueError("exposure must be 'indoor' or 'outdoor', got '{}'"
                             .format(exposure))
        self._exposure = exposure

        if domain not in ['physical', 'virtual']:
            raise ValueError("domain is required, must be 'physical' or 'virtual', got '{}'"
                             .format(domain))
        self._domain = domain

        if disposition is not None and disposition not in ['fixed', 'mobile']:
            raise ValueError("disposition must be 'fixed' or 'mobile', got '{}'"
                             .format(disposition))
        self._disposition = disposition

    def toeeml(self):
        """
        Convert this class into a EEML DOM element.

        :return: the location element
        :rtype: `Element`
        """

        loc = _elem('location')

        _addA(loc, self._exposure, 'exposure')
        _addA(loc, self._domain, 'domain')
        _addA(loc, self._disposition, 'disposition')
        _addE(loc, self._name, 'name')
        _addE(loc, self._lat, 'lat', str)
        _addE(loc, self._lon, 'lon', str)
        _addE(loc, self._ele, 'ele', str)

        return loc


class Data(object):
    """
    The Data element of the document
    """

    def __init__(self, id_, value, tags=list(), minValue=None, maxValue=None,
                 unit=None, at=None, datapoints=None):
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
        :param datapoints: additional datapoints beyond current_value
        :type datapoints: `DataPoint`
        """
        _assertPosInt(id_, 'id', True)
        self._id = id_
        self._value = value
        self._tags = tags
        
        self._minValue = minValue
        self._maxValue = maxValue
        if unit is not None and not isinstance(unit, Unit):
            raise ValueError("unit must be an instance of Unit, got {}"
                             .format(type(unit)))
        self._unit = unit
        if at is not None and not isinstance(at, datetime):
            raise ValueError("at must be an instance of datetime.datetime, "
                             "got {}".format(type(at)))
        self._at = at
        self._datapoints = datapoints

    def toeeml(self):
        """
        Convert this element into a DOM object.

        :return: a data element
        :rtype: `Element`
        """

        data = _elem('data')

        _addA(data, self._id, 'id', str)
        for tag in self._tags:
            _addE(data, tag, 'tag')

        if self._value is not None:
            tmp = _elem('current_value')
            _addA(tmp, self._minValue, 'minValue', str)
            _addA(tmp, self._maxValue, 'maxValue', str)
            _addA(tmp, self._at, 'at', lambda x: x.isoformat())
            tmp.text = str(self._value)
            data.append(tmp)

        if self._unit is not None:
            data.append(self._unit.toeeml())

        if self._datapoints is not None:
            data.append(self._datapoints.toeeml())
            
        return data


class DataPoints(object):
    """
    The DataPoints element of the document
    """

    def __init__(self, id_, values=list()):
        """
        Create a new DataPoints. We want to be able to simply add a DataPoints
        object to the Environment via updateData, so we have to specify the id
        of the Data object that will include this DataPoints.

        :param id_: This is the id of the Data object that this DataPoints will belong to
        :type id: positive `int`
        :param values: the value of the data points, pairs of (value, date), where date is optional
        :type values: `float`
        """
        _assertPosInt(id_, 'id', True)
        self._id = id_
        self._values = values
    
    def toeeml(self):
        """
        Convert this element into a DOM object.

        :return: a data element
        :rtype: `Element`
        """

        data = _elem('datapoints')

        for pair in self._values:
            tmp = _elem('value')
            tmp.text = str(pair[0])
            if len(pair) > 1:
                tmp.attrib['at'] = pair[1].isoformat()
            data.append(tmp)
            
        return data

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
    if loc is not None:
        env.setLocation(loc)
    eeml.setEnvironment(env)
    env.updateData(data)
    return eeml
