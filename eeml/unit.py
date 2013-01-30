"""
This package stores all the available implementations of Unit
"""

from eeml.util import _elem, _addA

class Unit(object):
    """
    This class represents a unit element in the EEML document.
    """

    __valid_types = ['basicSI', 'derivedSI', 'conversionBasedUnits',
                     'derivedUnits', 'contextDependentUnits']

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
        if type_ is not None and not type_ in self.__valid_types:
            raise ValueError("type must be {}, got '{}'".format(
                    ", ".join(['%s'%s for s in self.__valid_types]), type_))
        self._type = type_
        self._symbol = symbol

    def toeeml(self):
        """
        Convert this object into a DOM element.

        :return: the unit element
        :rtype: `Element`
        """

        unit = _elem('unit')

        _addA(unit, self._type, 'type')
        _addA(unit, self._symbol, 'symbol')

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

class Degree(Unit):
    """
    Degree of arc unit class.
    """

    def __init__(self):
        """
        Initialize the `Unit` parameters with Degree.
        """
        Unit.__init__(self, 'Degree', 'basicSI', u'\xb0')


class Fahrenheit(Unit):
    """
    Degree Fahrenheit unit class.
    """

    def __init__(self):
        """
        Initialize the `Unit` parameters with Fahrenheit.
        """
        Unit.__init__(self, 'Fahrenheit', 'derivedSI', u'\xb0F')


class hPa(Unit):
    """
    hPa unit class.
    """

    def __init__(self):
        """
        Initialize the `Unit` parameters with hPa.
        """
        Unit.__init__(self, 'hPa', 'derivedSI', 'hPa')


class Knots(Unit):
    """
    Knots class.
    """

    def __init__(self):
        """
        Initialize the `Unit` parameters with Knots.
        """
        Unit.__init__(self, 'Knots', 'conversionBasedUnits', u'kts')


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

