import eeml
import serial

# parameters
API_KEY = 'YOUR PERSONAL API KEY'
API_URL = 'YOUR PERSONAL API URL, LIKE /api/1275.xml'

serial = serial.Serial('/dev/ttyUSB0', 9600)
readings = serial.readline().strip().split(' ') # the readings are separated by spaces
pac = eeml.Pachube(API_URL, API_KEY)
pac.update([eeml.Data(0, readings[0], unit=eeml.Celsius()), eeml.Data(1, readings[1], unit=eeml.RH())])
pac.put()
