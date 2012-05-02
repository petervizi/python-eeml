from xml.etree import ElementTree as etree

from formencode.doctest_xml_compare import xml_compare

from nose.tools import assert_true

from eeml import *

from unittest import TestCase

class TestEEML(TestCase):

    def test_good_location(self):
        loc = Location('My Room', 32.4, 22.7, 0.2, 'indoor', 'physical', 'fixed')

        assert_true(xml_compare(etree.fromstring(
            """
            <location disposition="fixed" domain="physical" exposure="indoor">
            <name>My Room</name>
            <lat>32.4</lat>
            <lon>22.7</lon>
            <ele>0.2</ele>
            </location>
            """.strip()), loc.toeeml()))


    def test_good_unit(self):
        unit = Unit("Celcius", 'basicSI', "C")

        assert_true(xml_compare(etree.fromstring(
            """
            <unit type="basicSI" symbol="C">Celcius</unit>
            """.strip()), unit.toeeml()))


    def test_good_data(self):
        u = Unit('Celsius', 'derivedSI', 'C')
        test_data = Data(
            id=0,
            value=10.0, 
            tags=['length'], 
            minValue=0, 
            maxValue=100, 
            unit=u)

        assert_true(xml_compare(etree.fromstring(
            """
            <data id="0">
            <tag>length</tag>
            <value maxValue="100" minValue="0">10.0</value>
            <unit symbol="C" type="derivedSI">Celsius</unit>
            </data>
            """.strip()), test_data.toeeml()))


    def test_good_environment(self):
        env = Environment('A Room Somewhere',
            'http://www.pachube.com/feeds/1.xml',
            'frozen',
            'This is a room somewhere',
            'http://www.roomsomewhere/icon.png',
            'http://www.roomsomewhere/',
            'myemail@roomsomewhere',
            updated='2007-05-04T18:13:51.0Z',
            creator='http://www.haque.co.uk',
            id=1)

        assert_true(xml_compare(etree.fromstring(
            """
            <environment creator="http://www.haque.co.uk" id="1" updated="2007-05-04T18:13:51.0Z">
                <title>A Room Somewhere</title>
                <feed />
                <status>frozen</status>
                <description>This is a room somewhere</description>
                <icon>http://www.roomsomewhere/icon.png</icon>
                <website>http://www.roomsomewhere/</website>
                <email>myemail@roomsomewhere</email>
            </environment>""".strip()), env.toeeml()))

    def test_good_create_doc(self):
        env = Environment('A Room Somewhere',
            'http://www.pachube.com/feeds/1.xml',
            'frozen',
            'This is a room somewhere',
            'http://www.roomsomewhere/icon.png',
            'http://www.roomsomewhere/',
            'myemail@roomsomewhere',
            updated='2007-05-04T18:13:51.0Z',
            creator='http://www.haque.co.uk',
            id=1)
        loc = Location('My Room', 32.4, 22.7, 0.2, 'indoor', 'physical', 'fixed')
        u = Unit('Celsius', 'derivedSI', 'C')
        dat = []
        dat.append(Data(0, 36.2, minValue=23.8, maxValue=48.0, unit = u, tags=['temperature']))
        u = Unit('blushesPerHour', 'contextDependentUnits')
        dat.append(Data(1, 84.2, minValue=0, maxValue=100, unit = u, tags=['blush', 'redness', 'embarrasement']))
        u = Unit('meter', 'basicSI', 'm')
        dat.append(Data(2, 12.3, minValue=0, unit = u, tags=['length', 'distance', 'extension']))


        intermed = etree.tostring(
            create_eeml(env, loc, dat).toeeml()) # Broken down to help with error-checking
        final = etree.fromstring(intermed)

        assert_true(xml_compare(etree.fromstring(
            """
            <eeml version="5" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.eeml.org/xsd/005 http://www.eeml.org/xsd/005/005.xsd">
                <environment creator="http://www.haque.co.uk" id="1" updated="2007-05-04T18:13:51.0Z">
                    <title>A Room Somewhere</title>
                    <feed />
                    <status>frozen</status>
                    <description>This is a room somewhere</description>
                    <icon>http://www.roomsomewhere/icon.png</icon>
                    <website>http://www.roomsomewhere/</website>
                    <email>myemail@roomsomewhere</email>
                    <location disposition="fixed" domain="physical" exposure="indoor">
                        <name>My Room</name>
                        <lat>32.4</lat>
                        <lon>22.7</lon>
                        <ele>0.2</ele>
                    </location>
                    <data id="0">
                        <tag>temperature</tag>
                        <value maxValue="48.0" minValue="23.8">36.2</value>
                        <unit symbol="C" type="derivedSI">Celsius</unit>
                    </data>
                    <data id="1">
                        <tag>blush</tag>
                        <tag>redness</tag>
                        <tag>embarrasement</tag>
                        <value maxValue="100" minValue="0">84.2</value>
                        <unit type="contextDependentUnits">blushesPerHour</unit>
                    </data>
                    <data id="2">
                        <tag>length</tag>
                        <tag>distance</tag>
                        <tag>extension</tag>
                        <value minValue="0">12.3</value>
                        <unit symbol="m" type="basicSI">meter</unit>
                    </data>
                </environment>
            </eeml>
            """.strip()), final, reporter=self.fail))

