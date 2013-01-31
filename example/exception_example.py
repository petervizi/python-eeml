import eeml
import eeml.datastream
import eeml.unit
import serial
from eeml import CosmError

# parameters
API_KEY = 'YOUR PERSONAL API KEY'
FEED = 'YOUR PERSONAL FEED ID'
API_URL = '/v2/feeds/{feednum}.xml' .format(feednum = FEED)

serial = serial.Serial('/dev/ttyUSB0', 9600)
readings = serial.readline().strip().split(' ') # the readings are separated by spaces

# open up your cosm feed
pac = eeml.datastream.Cosm(API_URL, API_KEY)

# prepare the emml payload
pac.update([eeml.Data(0, readings[0], unit=eeml.unit.Celsius()), eeml.Data(1, readings[1], unit=eeml.unit.RH())])

# attempt to send the data to Cosm.  Attempt to handle exceptions, such that the script continues running.
# You could optionally place some retry logic around the pac.put() command.
try:
	pac.put()
except CosmError, e:
	print('ERROR: pac.put(): {}'.format(e))
except StandardError:
	print('ERROR: StandardError')
except:
	print('ERROR: Unexpected error: %s' % sys.exc_info()[0])
