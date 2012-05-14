import eeml
import serial
import datetime

a = datetime.tzinfo()

# parameters
API_KEY = 'YOUR_API_KEY'
# API_URL = '/v2/feeds/42166.xml'
API_URL = 42166

readings = [3, 4]
pac = eeml.Cosm(API_URL, API_KEY)
pac.update([
        eeml.Data("Temperature", readings[0], unit=eeml.Celsius()), 
        eeml.Data("Humidity", readings[1], unit=eeml.RH())])
pac.put()
