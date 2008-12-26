import constants
import ctypes

def getPendingMessageCount(queueName):
	admin = ctypes.c_void_p()
	status = constants.libtibemsadmin.tibemsAdmin_Create(ctypes.byref(admin), constants.serverUrl, 'admin', None, None)
	if status:
		print('Error creating admin: ' + str(status))
		return None

	TIBEMS_QUEUE = 1
	destinationInfo = ctypes.c_void_p()
	constants.libtibemsadmin.tibemsAdmin_GetDestination(admin, ctypes.byref(destinationInfo), queueName, TIBEMS_QUEUE)
	if status:
		print('Error getting desination info: ' + str(status))
		return None

	size = ctypes.c_int()
	constants.libtibemsadmin.tibemsDestinationInfo_GetPendingMessageCount(destinationInfo, ctypes.byref(size))
	if status:
		print('Error getting pending message count: ' + str(status))
		return None

	constants.libtibemsadmin.tibemsDestinationInfo_Destroy(destinationInfo)
	if status:
		print('Error destroying destination info: ' + str(status))
		return None
	
	status = constants.libtibemsadmin.tibemsAdmin_Close(admin)
	if status:
		print('Error closing admin: ' + str(status))
		return None

	return size.value

def purgeQueue(queueName):
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
	status = constants.libtibems.tibemsQueue_Create(ctypes.byref(destination), queueName)
	if status:
		print('Error creating queue: ' + str(status))
		return None

	session = ctypes.c_void_p()
	TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE=23
	status = constants.libtibems.tibemsConnection_CreateSession(connection, ctypes.byref(session), 0, TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE)
	if status:
		print('Error creating session: ' + str(status))
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

	for i in range(0, getPendingMessageCount(queueName)):
		message = ctypes.c_void_p()
		status = constants.libtibems.tibemsMsgConsumer_Receive(messageConsumer, ctypes.byref(message))
		if status:
			print('Error receiving message: ' + str(status))
			return None

		status = constants.libtibems.tibemsMsg_Acknowledge(message);
		if status:
			print('Error acknowledging message: ' + str(status))
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
