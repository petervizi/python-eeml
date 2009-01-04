import sys
from eeml import *
import httplib
import random

url = '/api/1275.xml'
key = 'f2a9bd5a63e6a397629ede7e44c80f6a0941ddecf9a986fed40aae95dab5392d'

pa = Pachube(url, key)
pa.update([Data(1, random.random(), unit=RH()), Data(0, random.random(), unit=Celsius())])
pa.put()
