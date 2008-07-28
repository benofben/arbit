def processWork(symbols, quotes):
        import cPickle
        import classifier
        import constants
        import ctypes

        factory = constants.libtibems.tibemsConnectionFactory_Create()
	if not factory:
		print 'Error creating factory: ' + str(status)
		return None

	status = constants.libtibems.tibemsConnectionFactory_SetServerURL(factory, constants.serverUrl)
	if status:
		print 'Error setting server URL: ' + str(status)
		return None

	connection = ctypes.c_void_p()
	status = constants.libtibems.tibemsConnectionFactory_CreateConnection(factory, ctypes.byref(connection), None, None)
	if status:
		print 'Error creating connection: ' + str(status)
		return None

	consumerDestination = ctypes.c_void_p()
	status = constants.libtibems.tibemsQueue_Create(ctypes.byref(consumerDestination), 'arbit.work.request')
	if status:
		print 'Error creating queue: ' + str(status)
		return None

        consumerSession = ctypes.c_void_p()
        TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE=23
	status = constants.libtibems.tibemsConnection_CreateSession(connection, ctypes.byref(consumerSession), 0, TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE)
	if status:
		print 'Error creating session: ' + str(status)
		return None

	messageConsumer = ctypes.c_void_p()
	status = constants.libtibems.tibemsSession_CreateConsumer(consumerSession, ctypes.byref(messageConsumer), consumerDestination, None, 0)
	if status:
		print 'Error creating consumer: ' + str(status)
		return False

	producerDestination = ctypes.c_void_p()
	status = constants.libtibems.tibemsQueue_Create(ctypes.byref(producerDestination), 'arbit.work.response')
	if status:
		print 'Error creating queue: ' + str(status)
		return None

        producerSession = ctypes.c_void_p()
	status = constants.libtibems.tibemsConnection_CreateSession(connection, ctypes.byref(producerSession), 0, TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE)
	if status:
		print 'Error creating session: ' + str(status)
		return None

	messageProducer = ctypes.c_void_p()
        status = constants.libtibems.tibemsSession_CreateProducer(producerSession, ctypes.byref(messageProducer), producerDestination)
	if status:
		print 'Error creating producer: ' + str(status)
		return False

	status = constants.libtibems.tibemsConnection_Start(connection)
	if status:
		print 'Error starting connection: ' + str(status)
		return False

	while(True):
		requestMessage = ctypes.c_void_p()
        	status = constants.libtibems.tibemsMsgConsumer_Receive(messageConsumer, ctypes.byref(requestMessage))
		if status:
			print 'Error receiving message: ' + str(status)
			return False

		messageType = ctypes.c_int()
	        status = constants.libtibems.tibemsMsg_GetBodyType(requestMessage, ctypes.byref(messageType))
		if status:
			print 'Error getting message type: ' + str(status)
			return False

		requestMessageText = ctypes.c_char_p()
		TIBEMS_TEXT_MESSAGE=6
		if messageType.value == TIBEMS_TEXT_MESSAGE:
			status = constants.libtibems.tibemsTextMsg_GetText(requestMessage, ctypes.byref(requestMessageText))
			if status:
				print 'Error getting message text: ' + str(status)
				return False
		else:
			print 'Error trying to get text from a nontext message.'
			return False
		
		request=cPickle.loads(requestMessageText.value)
		print "Processing " + request['Symbol'] + ' for day ' + str(request['Date']) +'.'

		my_classifier=classifier.classifier(request['Symbol'], request['Date'], quotes)
		p=my_classifier.run()

		response = {}
		response['p']=p
		response['Symbol']=request['Symbol']
		response['Date']=request['Date']
		responseMessageText=cPickle.dumps(response)

		responseMessage = ctypes.c_void_p()
                status = constants.libtibems.tibemsTextMsg_Create(ctypes.byref(responseMessage))
       		if status:
       			print 'Error creating message: ' + str(status)
       			return False

               	status = constants.libtibems.tibemsTextMsg_SetText(responseMessage, responseMessageText)
       		if status:
       			print 'Error setting message text: ' + str(status)
       			return False

         	status = constants.libtibems.tibemsMsgProducer_Send(messageProducer, responseMessage)
       		if status:
       			print 'Error sending message: ' + str(status)
       			return False

               	status = constants.libtibems.tibemsMsg_Destroy(responseMessage)
       		if status:
       			print 'Error destroying message: ' + str(status)
       			return False

		status = constants.libtibems.tibemsMsg_Acknowledge(requestMessage);
		if status:
			print 'Error acknowledging message: ' + str(status)
			return False

	        status = constants.libtibems.tibemsMsg_Destroy(requestMessage)
		if status:
			print 'Error destroying message: ' + str(status)
			return False

def run():
        print 'Starting client...'
        
	import data
	symbols=data.getSymbols()
	quotes=data.getAllQuotes()
	print 'Finished loading quotes.'

        print 'Processing work...'
        processWork(symbols, quotes)
        
run()
