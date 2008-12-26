take=0.02

import datetime
startDate=datetime.date(2008,8,1)
endDate=datetime.date.today()

import sys
import ctypes
platform = sys.platform
if platform == 'linux2':
	serverUrl='10.0.0.1'
	libtibems = ctypes.CDLL('libtibems.so')
	libtibemsadmin = ctypes.CDLL('libtibemsadmin.so')
elif platform == 'win32':
	serverUrl='127.0.0.1'
	libtibems = ctypes.CDLL('tibems.dll')
	libtibemsadmin = ctypes.CDLL('tibemsadmin.dll')
else:
	print('Sorry, I do not know which libraries to reference on ' + platform + '.')
	exit(1)
