def publishWorkRequests(symbols, quotes):
	import constants
	import ctypes
	import cPickle
	import datetime

	factory = constants.libtibems.tibemsConnectionFactory_Create()
	if not factory:
		print('Error creating factory: ' + str(status))
		return None

	status = constants.libtibems.tibemsConnectionFactory_SetServerURL(factory, constants.serverUrl)
	if status:
		print('Error setting server URL: ' + str(status))
		return None

	connection = ctypes.c_void_p()
	status = constants.libtibems.tibemsConnectionFactory_CreateConnection(factory, ctypes.byref(connection), None, None)
	if status:
		print('Error creating connection: ' + str(status))
		return None

	destination = ctypes.c_void_p()
	status = constants.libtibems.tibemsQueue_Create(ctypes.byref(destination), 'arbit.work.request')
	if status:
		print('Error creating queue: ' + str(status))
		return None

	session = ctypes.c_void_p()
	TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE=23
	status = constants.libtibems.tibemsConnection_CreateSession(connection, ctypes.byref(session), 0, TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE)
	if status:
		print('Error creating session: ' + str(status))
		return None

	messageProducer = ctypes.c_void_p()
	status = constants.libtibems.tibemsSession_CreateProducer(session, ctypes.byref(messageProducer), destination)
	if status:
		print('Error creating producer: ' + str(status))
		return None

	messageConsumer = ctypes.c_void_p()
	status = constants.libtibems.tibemsSession_CreateConsumer(session, ctypes.byref(messageConsumer), destination, None, 0)
	if status:
		print('Error creating consumer: ' + str(status))
		return None

	status = constants.libtibems.tibemsConnection_Start(connection)
	if status:
		print('Error starting connection: ' + str(status))
		return None

	for day in range(0, (constants.endDate-constants.startDate).days+1):
		date=constants.startDate+datetime.timedelta(days=day)
		for symbol in symbols:	
			request={}
			request['Symbol']=symbol
			request['Date']=date
			messageText=cPickle.dumps(request)

			message = ctypes.c_void_p()
			status = constants.libtibems.tibemsTextMsg_Create(ctypes.byref(message))
			if status:
				print('Error creating message: ' + str(status))
				return None

			status = constants.libtibems.tibemsTextMsg_SetText(message, messageText)
			if status:
				print('Error setting message text: ' + str(status))
				return None

			status = constants.libtibems.tibemsMsgProducer_Send(messageProducer, message)
			if status:
				print('Error sending message: ' + str(status))
				return None

			status = constants.libtibems.tibemsMsg_Destroy(message)
			if status:
				print('Error destroying message: ' + str(status))
				return None

	status = constants.libtibems.tibemsDestination_Destroy(destination)
	if status:
		print('Error destroying destination: ' + str(status))
		return None

	status = constants.libtibems.tibemsConnection_Close(connection)
	if status:
		print('Error closing connection: ' + str(status))
		return None

def cleanUp():
        import tibemsadmin
        tibemsadmin.purgeQueue('arbit.work.request')
        tibemsadmin.purgeQueue('arbit.work.response')

        import os
        if os.path.exists('data/response'):
                import shutil
                shutil.rmtree('data/response')
        os.makedirs('data/response')

def run():
	print('Cleaning up...')
	cleanUp()

	import data
	symbols=data.getSymbols()
	quotes=data.getAllQuotes()
	print('Finished loading quotes.')

	print('Sending work requests...')
	publishWorkRequests(symbols, quotes)

	print('All done.')

run()
