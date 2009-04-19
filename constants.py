take=0.02

import datetime
startDate=datetime.date(2009,2,1)
endDate=datetime.date.today()

# TIBCO EMS Library
import sys
import ctypes
platform = sys.platform
if platform == 'linux2':
	serverUrl='yesler'
	libtibems = ctypes.CDLL('libtibems.so')
	libtibemsadmin = ctypes.CDLL('libtibemsadmin.so')
elif platform == 'win32':
	serverUrl='127.0.0.1'
	libtibems = ctypes.CDLL('tibems.dll')
	libtibemsadmin = ctypes.CDLL('tibemsadmin.dll')
else:
	print 'Sorry, I do not know which libraries to reference on ' + platform + '.'
	exit(1)

# Ameritrade Login	
sourceID='LCK'
userid='benofdeth'
password='80trek80'

