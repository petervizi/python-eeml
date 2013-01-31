import eeml
import eeml.datastream
import eeml.unit
import serial
import datetime

# parameters
API_KEY = 'YOUR_API_KEY'
# API_URL = '/v2/feeds/42166.xml'
API_URL = 42166

readings = [3, 4]
pac = eeml.datastream.Cosm(API_URL, API_KEY)
at = datetime.datetime(2012, 9, 12, 11, 0, 0)

pac.update([
        eeml.Data(0, readings[0], tags=('Temperature',), unit=eeml.unit.Celsius(), at=at), 
        eeml.Data(1, readings[1], tags=('Humidity',), unit=eeml.unit.RH())])
pac.put()
print(pac.geteeml())
