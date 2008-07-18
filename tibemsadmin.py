serverUrl='localhost'

import sys
import ctypes

platform = sys.platform
if platform == 'linux2':
	libtibemsadmin = ctypes.CDLL('libtibemsadmin.so')
elif platform == 'win32':
	libtibemsadmin = ctypes.CDLL('tibemsadmin.dll')
else:
	print 'Sorry, I don\'t know which library to reference on ' + platform + '.'
	exit(1)

def getPendingMessageCount(queueName):
        admin = ctypes.c_void_p()
        status = libtibemsadmin.tibemsAdmin_Create(ctypes.byref(admin), serverUrl, 'admin', None, None)
        if status:
                print 'Error creating admin: ' + str(status)
                return None

        TIBEMS_QUEUE = 1
        destinationInfo = ctypes.c_void_p()
        libtibemsadmin.tibemsAdmin_GetDestination(admin, ctypes.byref(destinationInfo), queueName, TIBEMS_QUEUE)
        if status:
                print 'Error getting desination info: ' + str(status)
                return None

        size = ctypes.c_int()
        libtibemsadmin.tibemsDestinationInfo_GetPendingMessageCount(destinationInfo, ctypes.byref(size))
        if status:
                print 'Error getting pending message count: ' + str(status)
                return None

        libtibemsadmin.tibemsDestinationInfo_Destroy(destinationInfo)
        if status:
                print 'Error destroying destination info: ' + str(status)
                return None
        
        status = libtibemsadmin.tibemsAdmin_Close(admin)
        if status:
                print 'Error closing admin: ' + str(status)
                return None

        return size.value
