import datetime
startDate=datetime.date(2008,1,1)
endDate=datetime.date(2008,12,1)

serverUrl='localhost'

import sys
import ctypes
platform = sys.platform
if platform == 'linux2':
        libtibems = ctypes.CDLL('libtibems.so')
elif platform == 'win32':
        libtibems = ctypes.CDLL('tibems.dll')
else:
        print 'Sorry, I don\'t know which library to reference on ' + platform + '.'
        exit(1)

def run():
	import data
	symbols=data.getSymbols()
	quotes=data.getAllQuotes()
	print 'Finished loading quotes.'

        factory = libtibems.tibemsConnectionFactory_Create()
	if not factory:
		print 'Error creating factory: ' + str(status)
		return None

	status = libtibems.tibemsConnectionFactory_SetServerURL(factory, serverUrl)
	if status:
		print 'Error setting server URL: ' + str(status)
		return None

	connection = ctypes.c_void_p()
	status = libtibems.tibemsConnectionFactory_CreateConnection(factory, ctypes.byref(connection), None, None)
	if status:
		print 'Error creating connection: ' + str(status)
		return None

	destination = ctypes.c_void_p()
	status = libtibems.tibemsQueue_Create(ctypes.byref(destination), 'arbit.work.request')
	if status:
		print 'Error creating queue: ' + str(status)
		return None

        session = ctypes.c_void_p()
        TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE=23
	status = libtibems.tibemsConnection_CreateSession(connection, ctypes.byref(session), 0, TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE)
	if status:
		print 'Error creating session: ' + str(status)
		return None

	messageProducer = ctypes.c_void_p()
        status = libtibems.tibemsSession_CreateProducer(session, ctypes.byref(messageProducer), destination)
	if status:
		print 'Error creating producer: ' + str(status)
		return False

	########## should purge the queue before dumping new stuff in it!!!!!!!!!!!

	import cPickle
	for day in range(0, (endDate-startDate).days+1):
		date=startDate+datetime.timedelta(days=day)
		for symbol in symbols:	
			request={}
			request['Symbol']=symbol
			request['Date']=date
			messageText=cPickle.dumps(request)

        		message = ctypes.c_void_p()
        	        status = libtibems.tibemsTextMsg_Create(ctypes.byref(message))
        		if status:
        			print 'Error creating message: ' + str(status)
        			return False

                	status = libtibems.tibemsTextMsg_SetText(message, messageText)
        		if status:
        			print 'Error setting message text: ' + str(status)
        			return False

         		status = libtibems.tibemsMsgProducer_Send(messageProducer, message)
        		if status:
        			print 'Error sending message: ' + str(status)
        			return False

                	status = libtibems.tibemsMsg_Destroy(message)
        		if status:
        			print 'Error destroying message: ' + str(status)
        			return False

	status = libtibems.tibemsDestination_Destroy(destination)
	if status:
		print 'Error destroying destination: ' + str(status)
		return False

	status = libtibems.tibemsConnection_Close(connection)
	if status:
		print 'Error closing connection: ' + str(status)
		return False

	print 'Finished publishing work requests.'

run()
