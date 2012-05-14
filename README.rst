===========
python-eeml
===========

:authors: peter.vizi@gmail.com

Intorduction
============

This is a python package for generating eeml_ documents.

Installation
============

With administrative privileges run:
`sudo python setup.py install`

Without root access:
`python setup.py install --prefix=~/`
`PTYHONPATH="~/lib/python2.7/site-packages" python example/simple_example.py`

Example
=======

An example python script for publishing measurement data::

    import eeml
    import serial

    # parameters
    API_KEY = 'YOUR PERSONAL API KEY'
    API_URL = 'YOUR PERSONAL API URL, LIKE /api/1275.xml'

    serial = serial.Serial('/dev/ttyUSB0', 9600)
    readings = serial.readline().strip().split(' ') # the readings are separated by spaces
    pac = eeml.Cosm(API_URL, API_KEY)
    pac.update([eeml.Data(0, readings[0], unit=eeml.Celsius()), eeml.Data(1, readings[1], unit=eeml.RH())])
    pac.put()

Requirements
============

 * python-xml

.. _eeml: http://www.eeml.org/
