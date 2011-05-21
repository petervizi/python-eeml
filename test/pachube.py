import sys
from eeml import *
import httplib
import random

url = '/v2/feeds/1275.xml'
key = 'PACHUBE_API_KEY'

pa = Pachube(url, key)
pa.update([Data(1, random.random(), unit=RH()), Data(0, random.random(), unit=Celsius())])
pa.put()
