from xml.dom.minidom import *

class EEML:
    def __init__(self):
        self._environments = []

    def toeeml(self):
        doc = Document()
        eeml = doc.createElement('eeml')
        eeml.setAttribute('version', '5')
        eeml.setAttribute('xsi:schemaLocation', 'http://www.eeml.org/xsd/005 http://www.eeml.org/xsd/005/005.xsd')
        doc.appendChild(eeml)
        for env in self._environments:
            tmp = env.toeeml()
            eeml.appendChild(tmp)
        return doc

    def addEnvironment(self, env):
        if isinstance(env, Environment):
            self._environments.append(env)
        else:
            raise Exception()

class Environment:

    def __init__(self, title=None, feed=None, status=None, description=None,
                 icon=None, website=None, email=None, updated=None, creator=None, id=None):
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
        if isinstance(location, Location):
            self._location = location
        else:
            raise Exception

    def addData(self, data):
        if isinstance(data, Data):
            self._data.append(data)
        else:
            raise Exception()

    def toeeml(self):
        doc = Document()
        env = doc.createElement('environment')
        if self._updated:
            env.setAttribute('updated', self._updated.isoformat())
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
    def __init__(self, name=None, lat=None, lon=None, ele=None, exposure=None, domain=None, disposition=None):

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
            if disposition in ['fixed', 'fixed']:
                self._disposition = disposition
            else:
                raise Exception()

    def toeeml(self):
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
    def __init__(self, id, value, tags=[], minValue=None, maxValue=None, unit=None):
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
    def __init__(self, name, type=None, symbol=None):
        self._name = name
        if type:
            if type in ['basicSI', 'derivedSI', 'conversionBasedUnits', 'derivedUnits', 'contextDependentUnits']:
                self._type = type
            else:
                raise Exception()
        self._type = type
        self._symbol = symbol

    def toeeml(self):
        doc = Document()
        unit = doc.createElement('unit')
        if self._type:
            unit.setAttribute('type', self._type)
        if self._symbol:
            unit.setAttribute('symbol', self._symbol)

        unit.appendChild(doc.createTextNode(self._name))
        return unit

def echo(a):
    print a
