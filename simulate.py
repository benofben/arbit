import tibemsadmin
import cPickle

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

def receiveMessages():
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
	status = libtibems.tibemsQueue_Create(ctypes.byref(destination), 'arbit.work.response')
	if status:
		print 'Error creating queue: ' + str(status)
		return None

        session = ctypes.c_void_p()
        TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE=23
	status = libtibems.tibemsConnection_CreateSession(connection, ctypes.byref(session), 0, TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE)
	if status:
		print 'Error creating session: ' + str(status)
		return None

	messageConsumer = ctypes.c_void_p()
	status = libtibems.tibemsSession_CreateConsumer(session, ctypes.byref(messageConsumer), destination, None, 0)
	if status:
		print 'Error creating consumer: ' + str(status)
		return False

        status = libtibems.tibemsConnection_Start(connection)
	if status:
		print 'Error starting connection: ' + str(status)
		return False

        for i in range(0, tibemsadmin.getPendingMessageCount('arbit.work.response')):
	
                message = ctypes.c_void_p()
                status = libtibems.tibemsMsgConsumer_Receive(messageConsumer, ctypes.byref(message))
                if status:
                        print 'Error receiving message: ' + str(status)
                        return False

                messageType = ctypes.c_int()
                status = libtibems.tibemsMsg_GetBodyType(message, ctypes.byref(messageType))
                if status:
                        print 'Error getting message type: ' + str(status)
                        return False

                messageText = ctypes.c_char_p()
                TIBEMS_TEXT_MESSAGE=6
                if messageType.value == TIBEMS_TEXT_MESSAGE:
                        status = libtibems.tibemsTextMsg_GetText(message, ctypes.byref(messageText))
                        if status:
                                print 'Error getting message text: ' + str(status)
                                return False
        	else:
        		print  'Error trying to get text from a nontext message.'
        		return False
		
                request=cPickle.loads(messageText.value)
                filename='data/response/' + str(request['Date']) + request['Symbol']
                f=open(filename, 'w')
                cPickle.dump(request, f)
                f.close()
        
                status = libtibems.tibemsMsg_Acknowledge(message);
                if status:
                        print 'Error acknowledging message: ' + str(status)
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

def main():
        import os
        if not os.path.exists('data/response'):
                os.makedirs('data/response')
                
        receiveMessages()
        print 'Finished receiving messages.'
        
	import datetime
	startDate=datetime.date(2008,1,1)
	endDate=datetime.date(2009,1,1)

	import data
	symbols=data.getSymbols()
	quotes=data.getAllQuotes()
	print 'Finished loading quotes.'
	
	c=25000
	wins=0
	total=0
	
	for day in range(0, (endDate-startDate).days):
		currentDate=startDate+datetime.timedelta(days=day)

		best_p_vgood=0
		best_symbol=''

		for symbol in symbols:
			# for this symbol, we need the last date the symbol was traded
			index=data.getIndex(currentDate, quotes[symbol])
			if index:
				date=quotes[symbol]['Date'][index-1]
				filename='data/response/' + str(date) + symbol
				if os.path.exists(filename):
					f = open(filename, 'r')
					response=cPickle.load(f)
					p=response['p']

					if p['Good']>best_p_vgood:
						best_p_vgood=p['Good']
						best_symbol=symbol

		# see how we did for today
		if best_symbol:
			index=data.getIndex(currentDate, quotes[best_symbol])

			Open=quotes[best_symbol]['Open'][index]
			Close=quotes[best_symbol]['Close'][index]
			High=quotes[best_symbol]['High'][index]
		
			if High>Open*1.02:
				c=c*1.02
				wins=wins+1
			else:
				c=c*(Close/Open)
			total=total+1
		
			pwin=float(wins)/total
			print str(currentDate) + '\t' \
			+ str(round(c)) +  '\t' \
			+ best_symbol +  '\t' \
			+ str(round(best_p_vgood,5)) + '\t' \
			+ str(round(pwin,5)) + '\t'

main()
