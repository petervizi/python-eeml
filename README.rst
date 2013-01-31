===========
python-eeml
===========

:authors: peter.vizi@gmail.com

.. image:: https://travis-ci.org/petervizi/python-eeml.png?branch=master
   :target: https://travis-ci.org/petervizi/python-eeml

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
    import eeml.datastream
    import eeml.unit
    import serial

    # parameters
    API_KEY = 'YOUR PERSONAL API KEY'
    API_URL = 'YOUR PERSONAL API URL, LIKE /api/1275.xml'

    serial = serial.Serial('/dev/ttyUSB0', 9600)
    readings = serial.readline().strip().split(' ') # the readings are separated by spaces
    pac = eeml.datastream.Cosm(API_URL, API_KEY)
    pac.update([eeml.Data(0, readings[0], unit=eeml.unit.Celsius()), eeml.Data(1, readings[1], unit=eeml.unit.RH())])
    pac.put()

Other examples can be found in the example folder.

Requirements
============

 * python-xml

.. _eeml: http://www.eeml.org/
