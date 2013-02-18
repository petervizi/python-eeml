from datetime import datetime
import pytz

from lxml import etree

from formencode.doctest_xml_compare import xml_compare

from nose.tools import assert_true

from eeml import Location, EEML, Environment, Data, DataPoints, create_eeml
from eeml.datastream import Cosm, Pachube
from eeml.unit import Celsius, Unit, RH

from unittest import TestCase
from unittest import main as UnitTestMain

class TestEEML(TestCase):

    def test_good_location(self):
        loc = Location('physical', 'My Room', 32.4, 22.7, 0.2, 'indoor', 'fixed')

        assert_true(xml_compare(etree.fromstring(
            """
            <location xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.eeml.org/xsd/0.5.1" disposition="fixed" domain="physical" exposure="indoor">
            <name>My Room</name>
            <lat>32.4</lat>
            <lon>22.7</lon>
            <ele>0.2</ele>
            </location>
            """), loc.toeeml(), reporter=self.fail))


    def test_good_unit(self):
        unit = Unit("Celzius", 'basicSI', "C")

        assert_true(xml_compare(etree.fromstring(
            """
            <unit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.eeml.org/xsd/0.5.1" type="basicSI" symbol="C">Celzius</unit>
            """), unit.toeeml(), reporter=self.fail))


    def test_good_data(self):
        u = Unit('Celsius', 'derivedSI', 'C')
        test_data = Data(
            id_=0,
            value=10.0, 
            tags=['length', 'foo'], 
            minValue=0, 
            maxValue=100, 
            unit=u)

        assert_true(xml_compare(etree.fromstring(
            """
            <data xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.eeml.org/xsd/0.5.1" id="0">
            <tag>length</tag>
            <tag>foo</tag>
            <current_value maxValue="100" minValue="0">10.0</current_value>
            <unit symbol="C" type="derivedSI">Celsius</unit>
            </data>
            """), test_data.toeeml(), reporter=self.fail))


    def test_good_datapoints(self):
        env = Environment('A Room Somewhere',
                          'http://www.cosm.com/feeds/1.xml',
                          'frozen',
                          'This is a room somewhere',
                          'http://www.roomsomewhere/icon.png',
                          'http://www.roomsomewhere/',
                          'myemail@roomsomewhere',
                          updated=datetime(2007, 5, 4, 18, 13, 51, 0, pytz.utc),
                          creator='http://www.somewhere',
                          id_=1)

        datapoints = DataPoints(1, [(0,), (1,), (2, datetime(2007, 5, 4, 18, 13, 51, 0, pytz.utc))])

        result = create_eeml(env, None, datapoints).toeeml()

        assert_true(xml_compare(etree.fromstring(
            """
<eeml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.eeml.org/xsd/0.5.1" xsi:schemaLocation="http://www.eeml.org/xsd/0.5.1 http://www.eeml.org/xsd/0.5.1/0.5.1.xsd" version="0.5.1">
  <environment updated="2007-05-04T18:13:51+00:00" creator="http://www.somewhere" id="1">
    <title>A Room Somewhere</title>
    <feed>http://www.cosm.com/feeds/1.xml</feed>
    <status>frozen</status>
    <description>This is a room somewhere</description>
    <icon>http://www.roomsomewhere/icon.png</icon>
    <website>http://www.roomsomewhere/</website>
    <email>myemail@roomsomewhere</email>
    <data id="1">
      <datapoints xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.eeml.org/xsd/0.5.1">
        <value>0</value>
        <value>1</value>
        <value at="2007-05-04T18:13:51+00:00">2</value>
      </datapoints>
    </data>
  </environment>
</eeml>
"""), result, reporter=self.fail))


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
            id_=1)

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
            </environment>"""), env.toeeml(), reporter=self.fail))

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
            id_=1)
        loc = Location('physical', 'My Room', 32.4, 22.7, 0.2, 'indoor', 'fixed')
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
            """), final, reporter=self.fail))

    def test_status(self):
        Environment(status='frozen')
        Environment(status='live')
        with self.assertRaises(ValueError):
            Environment(status='foobar')

    def test_env_location(self):
        env = Environment()
        env.setLocation(Location('virtual'))
        with self.assertRaises(ValueError):
            env.setLocation('foobar')

    def test_env_id(self):
        Environment(id_=1)
        Environment(id_=None)
        with self.assertRaises(ValueError):
            Environment(id_='foobar')
        with self.assertRaises(ValueError):
            Environment(id_=4.22)

    def test_env_private(self):
        env = Environment(private=False)
        assert_true(xml_compare(etree.fromstring("""
<environment xmlns="http://www.eeml.org/xsd/0.5.1">
  <private>false</private>
</environment>"""), env.toeeml(), reporter=self.fail))

        env = Environment(private=True)
        assert_true(xml_compare(etree.fromstring("""
<environment xmlns="http://www.eeml.org/xsd/0.5.1">
  <private>true</private>
</environment>"""), env.toeeml(), reporter=self.fail))

        with self.assertRaises(ValueError):
            Environment(private='foobar')

    def test_eeml_ctor(self):
        EEML(Environment())
        with self.assertRaises(ValueError):
            EEML('foobar')

    def test_exposure(self):
        Location('virtual', exposure='indoor')
        Location('physical', exposure='outdoor')
        with self.assertRaises(ValueError):
            Location('virtual', exposure='foobar')

    def test_domain(self):
        Location(domain='physical')
        Location(domain='virtual')
        Location('physical')
        Location('virtual')
        with self.assertRaises(ValueError):
            Location(domain='foobar')
        with self.assertRaises(ValueError):
            Location('foobar')

    def test_disposition(self):
        Location('virtual', disposition='fixed')
        Location('virtual', disposition='mobile')
        with self.assertRaises(ValueError):
            Location('virtual', disposition='foobar')

    def test_unit(self):
        Data(1, 2, unit=None)
        Data(1, 2, unit=Celsius())
        with self.assertRaises(ValueError):
            Data(1, 2, unit='foobar')

    def test_at(self):
        Data(1, 2, at=datetime.now())
        with self.assertRaises(ValueError):
            Data(1, 2, at='foobar')

    def test_data_id(self):
        Data(1, 2)
        with self.assertRaises(ValueError):
            Data('foobar', 4)
        with self.assertRaises(ValueError):
            Data(4.44, 4)

    def test_unit_types(self):
        for i in ['basicSI', 'derivedSI', 'conversionBasedUnits',
                  'derivedUnits', 'contextDependentUnits']:
            Unit('foobar', i)
        with self.assertRaises(ValueError):
            Unit('foobar', 'barbar')

    def test_pachube(self):
        Pachube('/v2/feeds/1234.xml', 'ASDF')
        Pachube(1234, 'ASDF')
        with self.assertRaises(ValueError):
            Pachube('12.xml', 'ASDF')

    def test_cosm(self):
        Cosm('/v2/feeds/1234.xml', 'ASDF')
        Cosm(1234, 'ASDF')
        with self.assertRaises(ValueError):
            Cosm('api.cosm.com/v2/feeds/', 'ASDF')
        
    def test_multiple_datapoints(self):
        env = Environment()
        env.updateData(DataPoints(1, [(4,)]))
        env.updateData(DataPoints(4, [(5,)]))
        env.updateData(DataPoints(1, [(6,), (7,)]))

        assert_true(xml_compare(etree.fromstring("""
<environment xmlns="http://www.eeml.org/xsd/0.5.1">
  <data id="1">
    <datapoints>
      <value>6</value>
      <value>7</value>
    </datapoints>
  </data>
  <data id="4">
    <datapoints>
      <value>5</value>
    </datapoints>
  </data>
</environment>"""), env.toeeml(), reporter=self.fail))

    def test_multiple_update(self):
        pac = Cosm(1, 'ASDF')
        pac.update([
                Data(1, 10),
                Data(2, 22, unit=RH()),
                Data(3, 44),
                Data(5, 65)])

        pac.update([
                Data(2, 476),
                Data(5, -1)])

        assert_true(xml_compare(etree.fromstring("""
            <eeml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.eeml.org/xsd/0.5.1" xsi:schemaLocation="http://www.eeml.org/xsd/0.5.1 http://www.eeml.org/xsd/0.5.1/0.5.1.xsd" version="0.5.1">
              <environment>
                <data id="1">
                  <current_value>10</current_value>
                </data>
                <data id="2">
                  <current_value>476</current_value>
                </data>
                <data id="3">
                  <current_value>44</current_value>
                </data>
                <data id="5">
                  <current_value>-1</current_value>
                </data>
              </environment>
            </eeml>"""),
                                etree.fromstring(pac.geteeml()), reporter=self.fail))

    def test_invalidator(self):
        import eeml.validator
        oldvalidator = eeml.validator
        from eeml.invalidator import Invalidator
        eeml.validator = Invalidator()
        env = Environment(status='foobar')
        eeml.validator = oldvalidator
