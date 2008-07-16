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

# Since this is python, we can't include header files.
# Here are a couple useful definitions.

# acknowledgement types
TIBEMS_SESSION_TRANSACTED                   = 0
TIBEMS_AUTO_ACKNOWLEDGE                     = 1
TIBEMS_CLIENT_ACKNOWLEDGE                   = 2
TIBEMS_DUPS_OK_ACKNOWLEDGE                  = 3
TIBEMS_NO_ACKNOWLEDGE                       = 22
TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE          = 23
TIBEMS_EXPLICIT_CLIENT_DUPS_OK_ACKNOWLEDGE  = 24

# message types
TIBEMS_MESSAGE_UNKNOWN                      = 0
TIBEMS_MESSAGE                              = 1
TIBEMS_BYTES_MESSAGE                        = 2
TIBEMS_MAP_MESSAGE                          = 3
TIBEMS_OBJECT_MESSAGE                       = 4
TIBEMS_STREAM_MESSAGE                       = 5
TIBEMS_TEXT_MESSAGE                         = 6
TIBEMS_MESSAGE_UNDEFINED                    = 256

class tibems:
	userName = None
	password = None	
	serverUrl = None
	ackMode=TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE

	connection = ctypes.c_void_p()
	destination = ctypes.c_void_p()
	session = ctypes.c_void_p()

	def start(self, queueName):
		factory = libtibems.tibemsConnectionFactory_Create()
		if not factory:
			print 'Error creating factory: ' + str(status)
			return False

		status = libtibems.tibemsConnectionFactory_SetServerURL(factory, self.serverUrl)
		if status:
			print 'Error setting server URL: ' + str(status)
			return False

		status = libtibems.tibemsConnectionFactory_CreateConnection(factory, ctypes.byref(self.connection), self.userName, self.password)
		if status:
			print 'Error creating connection: ' + str(status)
			return False

		status = libtibems.tibemsQueue_Create(ctypes.byref(self.destination), queueName)
		if status:
			print 'Error creating queue: ' + str(status)
			return False

		status = libtibems.tibemsConnection_CreateSession(self.connection, ctypes.byref(self.session), 0, self.ackMode)
		if status:
			print 'Error creating session: ' + str(status)
			return False
	
		return True

	def stop(self):
		status = libtibems.tibemsDestination_Destroy(self.destination)
		if status:
			print 'Error destroying destination: ' + str(status)
			return False

		status = libtibems.tibemsConnection_Close(self.connection)
		if status:
			print 'Error closing connection: ' + str(status)
			return False

		return True

	def sendMessage(self, messageText):
		messageProducer = ctypes.c_void_p()
		message = ctypes.c_void_p()

		status = libtibems.tibemsSession_CreateProducer(self.session, ctypes.byref(messageProducer), self.destination)
		if status:
			print 'Error creating producer: ' + str(status)
			return False

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

		return True

	def receiveMessage(self):
		messageConsumer = ctypes.c_void_p()
		message = ctypes.c_void_p()

		status = libtibems.tibemsSession_CreateConsumer(self.session, ctypes.byref(messageConsumer), self.destination, None, 0)
		if status:
			print 'Error creating consumer: ' + str(status)
			return False

		status = libtibems.tibemsConnection_Start(self.connection)
		if status:
			print 'Error starting connection: ' + str(status)
			return False
	
        	status = libtibems.tibemsMsgConsumer_Receive(messageConsumer, ctypes.byref(message))
		if status:
			print 'Error receiving message: ' + str(status)
			return False

		return message

	def acknowledgeAndDestroyMessage(self, message):
		status = libtibems.tibemsMsg_Acknowledge(message);
		if status:
			print 'Error acknowledging message: ' + str(status)
			return False

	        status = libtibems.tibemsMsg_Destroy(message)
		if status:
			print 'Error destroying message: ' + str(status)
			return False

		return True

	def getMessageText(self, message):
		messageType = ctypes.c_int()
		messageText = ctypes.c_char_p()

	        status = libtibems.tibemsMsg_GetBodyType(message, ctypes.byref(messageType))
		if status:
			print 'Error getting message type: ' + str(status)
			return False

		if messageType.value == TIBEMS_TEXT_MESSAGE:
			status = libtibems.tibemsTextMsg_GetText(message, ctypes.byref(messageText))
			if status:
				print 'Error getting message text: ' + str(status)
				return False
		else:
			print 'Error trying to get text from a nontext message.'
			return False
	
		return messageText.value

queueName='foo'
te = tibems()
te.start(queueName)
te.sendMessage('bar')
message = te.receiveMessage()
messageText = te.getMessageText(message)
if messageText:
	print 'I got a message: ' + messageText
te.acknowledgeAndDestroyMessage(message)
te.stop()

