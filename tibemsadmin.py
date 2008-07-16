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

def run():
    admin = ctypes.c_void_p()
    status = libtibemsadmin.tibemsAdmin_Create(ctypes.byref(admin), serverUrl, 'admin', None, None)
    if status:
        print 'Error creating admin: ' + str(status)
        return None


    serverInfo = ctypes.c_void_p()
    status = libtibemsadmin.tibemsAdmin_GetInfo(admin, ctypes.byref(serverInfo))


    libtibemsadmin.tibemsAdmin_Close()  
    libtibemsadmin.tibemsAdmin_Create()
    libtibemsadmin.tibemsAdmin_GetCommandTimeout()
    libtibemsadmin.tibemsAdmin_GetConsumer()
    libtibemsadmin.tibemsAdmin_GetConsumers()
    libtibemsadmin.tibemsAdmin_GetInfo()
    libtibemsadmin.tibemsAdmin_GetProducerStatistics()
    #libtibemsadmin.tibemsAdmin_GetQueue()
    #libtibemsadmin.tibemsAdmin_GetQueues()
    #libtibemsadmin.tibemsAdmin_GetTopic()
    #libtibemsadmin.tibemsAdmin_GetTopics()
    libtibemsadmin.tibemsAdmin_SetCommandTimeout()


    queueInfo = ctypes.c_void_p()
    status = libtibemsadmin.tibemsAdmin_GetQueue(admin, queueInfo, 'arbit.work.response')
    if status:
        print 'Error getting queue: ' + str(status)
        return None

    status = libtibemsadmin.tibemsAdmin_Close(admin)
    if status:
        print 'Error closing admin: ' + str(status)
        return None

run()
