import eeml
import serial
import datetime

a = datetime.tzinfo()

# parameters
API_KEY = 'f2a9bd5a63e6a397629ede7e44c80f6a0941ddecf9a986fed40aae95dab5392d'
API_URL = '/api/1275.xml'
#API_URL = 

readings = [3, 4]
pac = eeml.Pachube(API_URL, API_KEY)
pac.update([eeml.Data(0, readings[0], unit=eeml.Celsius()), eeml.Data(1, readings[1], unit=eeml.RH())])
pac.put()
