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
            <location xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.eeml.org/xsd/0.5.1" disposition="fixed" domain="physical" exposure="indoor">
            <name>My Room</name>
            <lat>32.4</lat>
            <lon>22.7</lon>
            <ele>0.2</ele>
            </location>
            """.strip()), loc.toeeml(), reporter=self.fail))


    def test_good_unit(self):
        unit = Unit("Celzius", 'basicSI', "C")

        assert_true(xml_compare(etree.fromstring(
            """
            <unit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.eeml.org/xsd/0.5.1" type="basicSI" symbol="C">Celzius</unit>
            """.strip()), unit.toeeml(), reporter=self.fail))


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
            <data xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.eeml.org/xsd/0.5.1" id="0">
            <tag>length</tag>
            <current_value maxValue="100" minValue="0">10.0</current_value>
            <unit symbol="C" type="derivedSI">Celsius</unit>
            </data>
            """.strip()), test_data.toeeml(), reporter=self.fail))


    def test_good_datapoints(self):
        env = Environment('A Room Somewhere',
                          'http://www.cosm.com/feeds/1.xml',
                          'frozen',
                          'This is a room somewhere',
                          'http://www.roomsomewhere/icon.png',
                          'http://www.roomsomewhere/',
                          'myemail@roomsomewhere',
                          updated='2007-05-04T18:13:51.0Z',
                          creator='http://www.somewhere',
                          id=1)

        datapoints = DataPoints([(0,), (1,), (2, datetime(2007, 5, 4, 18, 13, 51))])

        result = create_eeml(env, None, datapoints).toeeml()

        assert_true(xml_compare(etree.fromstring(
            """
<eeml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.eeml.org/xsd/0.5.1" xsi:schemaLocation="http://www.eeml.org/xsd/0.5.1 http://www.eeml.org/xsd/0.5.1/0.5.1.xsd" version="0.5.1">
  <environment updated="2007-05-04T18:13:51.0Z" creator="http://www.somewhere" id="1">
    <title>A Room Somewhere</title>
    <feed>http://www.cosm.com/feeds/1.xml</feed>
    <status>frozen</status>
    <description>This is a room somewhere</description>
    <icon>http://www.roomsomewhere/icon.png</icon>
    <website>http://www.roomsomewhere/</website>
    <email>myemail@roomsomewhere</email>
    <data>
      <datapoints xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.eeml.org/xsd/0.5.1">
        <value>0</value>
        <value>1</value>
        <value at="2007-05-04T18:13:51">2</value>
      </datapoints>
    </data>
  </environment>
</eeml>
""".strip()), result, reporter=self.fail))


    def test_good_environment(self):
        env = Environment('A Room Somewhere',
            'http://www.cosm.com/feeds/1.xml',
            'frozen',
            'This is a room somewhere',
            'http://www.roomsomewhere/icon.png',
            'http://www.roomsomewhere/',
            'myemail@roomsomewhere',
            updated='2007-05-04T18:13:51.0Z',
            creator='http://www.somewhere',
            id=1)

        assert_true(xml_compare(etree.fromstring(
            """
            <environment xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.eeml.org/xsd/0.5.1" creator="http://www.somewhere" id="1" updated="2007-05-04T18:13:51.0Z">
                <title>A Room Somewhere</title>
                <feed>http://www.cosm.com/feeds/1.xml</feed>
                <status>frozen</status>
                <description>This is a room somewhere</description>
                <icon>http://www.roomsomewhere/icon.png</icon>
                <website>http://www.roomsomewhere/</website>
                <email>myemail@roomsomewhere</email>
            </environment>""".strip()), env.toeeml(), reporter=self.fail))

    def test_good_create_doc(self):
        env = Environment('A Room Somewhere',
            'http://www.cosm.com/feeds/1.xml',
            'frozen',
            'This is a room somewhere',
            'http://www.roomsomewhere/icon.png',
            'http://www.roomsomewhere/',
            'myemail@roomsomewhere',
            updated='2007-05-04T18:13:51.0Z',
            creator='http://www.somewhere',
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
            <eeml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.eeml.org/xsd/0.5.1" xsi:schemaLocation="http://www.eeml.org/xsd/0.5.1 http://www.eeml.org/xsd/0.5.1/0.5.1.xsd" version="0.5.1">
                <environment creator="http://www.somewhere" id="1" updated="2007-05-04T18:13:51.0Z">
                    <title>A Room Somewhere</title>
                    <feed>http://www.cosm.com/feeds/1.xml</feed>                    
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
                        <current_value maxValue="48.0" minValue="23.8">36.2</current_value>
                        <unit symbol="C" type="derivedSI">Celsius</unit>
                    </data>
                    <data id="1">
                        <tag>blush</tag>
                        <tag>redness</tag>
                        <tag>embarrasement</tag>
                        <current_value maxValue="100" minValue="0">84.2</current_value>
                        <unit type="contextDependentUnits">blushesPerHour</unit>
                    </data>
                    <data id="2">
                        <tag>length</tag>
                        <tag>distance</tag>
                        <tag>extension</tag>
                        <current_value minValue="0">12.3</current_value>
                        <unit symbol="m" type="basicSI">meter</unit>
                    </data>
                </environment>
            </eeml>
            """.strip()), final, reporter=self.fail))

