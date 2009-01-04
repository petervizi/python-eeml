import sys
from eeml import *
import httplib
import random

url = '/api/1275.xml'
key = 'f2a9bd5a63e6a397629ede7e44c80f6a0941ddecf9a986fed40aae95dab5392d'

data = [Data(0, random.random(), unit=Celsius()), Data(1, random.random(), unit=RH())]

eeml = create_eeml(Environment(), None, data).toeeml()


conn = httplib.HTTPConnection('www.pachube.com')
conn.set_debuglevel(9)


conn.request('PUT', url, eeml.toxml(), {'X-PachubeApiKey': key})

resp = conn.getresponse()

print resp.status, resp.reason

data = resp.read()
print data

conn.close()
