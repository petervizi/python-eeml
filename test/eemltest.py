from eeml import *
from datetime import datetime

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

print create_eeml(env, loc, dat).toeeml().toprettyxml(indent="  ")
