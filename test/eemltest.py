from eeml import *
from datetime import datetime

a = Environment('title', 'feed', 'frozen', 'desc', 'icon', 'website', 'email', updated=datetime.now(), creator='bela', id=1)
e = EEML()
l = Location('My Room', 32.4, 22.7, 0.2, 'indoor', 'physical', 'fixed')
u = Unit('blushesPerHour', 'contextDependentUnits')
d = Data(1, 1, minValue=-10, maxValue=20, unit = u)
a.setLocation(l)
e.addEnvironment(a)

a.addData(d)


print e.toeeml().toprettyxml(indent="  ")
