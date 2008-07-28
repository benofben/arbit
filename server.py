import constants
import tibemsadmin

import ctypes
import sys

import cPickle
import datetime

def run():
	import data
	symbols=data.getSymbols()
	quotes=data.getAllQuotes()
	print 'Finished loading quotes.'

	platform = sys.platform
        if platform == 'linux2':
                libtibems = ctypes.CDLL('libtibems.so')
        elif platform == 'win32':
                libtibems = ctypes.CDLL('tibems.dll')

        factory = libtibems.tibemsConnectionFactory_Create()
	if not factory:
		print 'Error creating factory: ' + str(status)
		return None

	status = libtibems.tibemsConnectionFactory_SetServerURL(factory, constants.serverUrl)
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
		return None

	messageConsumer = ctypes.c_void_p()
	status = libtibems.tibemsSession_CreateConsumer(session, ctypes.byref(messageConsumer), destination, None, 0)
	if status:
		print 'Error creating consumer: ' + str(status)
		return None

	status = libtibems.tibemsConnection_Start(connection)
	if status:
		print 'Error starting connection: ' + str(status)
		return None

        for i in range(0, tibemsadmin.getPendingMessageCount('arbit.work.request')):
                message = ctypes.c_void_p()
        	status = libtibems.tibemsMsgConsumer_Receive(messageConsumer, ctypes.byref(message))
		if status:
			print 'Error receiving message: ' + str(status)
			return None

		status = libtibems.tibemsMsg_Acknowledge(message);
		if status:
			print 'Error acknowledging message: ' + str(status)
			return None

	        status = libtibems.tibemsMsg_Destroy(message)
		if status:
			print 'Error destroying message: ' + str(status)
			return None
        
	for day in range(0, (constants.endDate-constants.startDate).days+1):
		date=constants.startDate+datetime.timedelta(days=day)
		for symbol in symbols:	
			request={}
			request['Symbol']=symbol
			request['Date']=date
			messageText=cPickle.dumps(request)

        		message = ctypes.c_void_p()
        	        status = libtibems.tibemsTextMsg_Create(ctypes.byref(message))
        		if status:
        			print 'Error creating message: ' + str(status)
        			return None

                	status = libtibems.tibemsTextMsg_SetText(message, messageText)
        		if status:
        			print 'Error setting message text: ' + str(status)
        			return None

         		status = libtibems.tibemsMsgProducer_Send(messageProducer, message)
        		if status:
        			print 'Error sending message: ' + str(status)
        			return None

                	status = libtibems.tibemsMsg_Destroy(message)
        		if status:
        			print 'Error destroying message: ' + str(status)
        			return None

	status = libtibems.tibemsDestination_Destroy(destination)
	if status:
		print 'Error destroying destination: ' + str(status)
		return None

	status = libtibems.tibemsConnection_Close(connection)
	if status:
		print 'Error closing connection: ' + str(status)
		return None

	print 'Finished publishing work requests.'

run()
