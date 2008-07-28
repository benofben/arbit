import tibemsadmin
import cPickle
import datetime
import constants
import ctypes

def receiveMessages():
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

	destination = ctypes.c_void_p()
	status = constants.libtibems.tibemsQueue_Create(ctypes.byref(destination), 'arbit.work.response')
	if status:
		print 'Error creating queue: ' + str(status)
		return None

        session = ctypes.c_void_p()
        TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE=23
	status = constants.libtibems.tibemsConnection_CreateSession(connection, ctypes.byref(session), 0, TIBEMS_EXPLICIT_CLIENT_ACKNOWLEDGE)
	if status:
		print 'Error creating session: ' + str(status)
		return None

	messageConsumer = ctypes.c_void_p()
	status = constants.libtibems.tibemsSession_CreateConsumer(session, ctypes.byref(messageConsumer), destination, None, 0)
	if status:
		print 'Error creating consumer: ' + str(status)
		return False

        status = constants.libtibems.tibemsConnection_Start(connection)
	if status:
		print 'Error starting connection: ' + str(status)
		return False

        for i in range(0, tibemsadmin.getPendingMessageCount('arbit.work.response')):
	
                message = ctypes.c_void_p()
                status = constants.libtibems.tibemsMsgConsumer_Receive(messageConsumer, ctypes.byref(message))
                if status:
                        print 'Error receiving message: ' + str(status)
                        return False

                messageType = ctypes.c_int()
                status = constants.libtibems.tibemsMsg_GetBodyType(message, ctypes.byref(messageType))
                if status:
                        print 'Error getting message type: ' + str(status)
                        return False

                messageText = ctypes.c_char_p()
                TIBEMS_TEXT_MESSAGE=6
                if messageType.value == TIBEMS_TEXT_MESSAGE:
                        status = constants.libtibems.tibemsTextMsg_GetText(message, ctypes.byref(messageText))
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
        
                status = constants.libtibems.tibemsMsg_Acknowledge(message);
                if status:
                        print 'Error acknowledging message: ' + str(status)
                        return False

                status = constants.libtibems.tibemsMsg_Destroy(message)
                if status:
                        print 'Error destroying message: ' + str(status)
                        return False

	status = constants.libtibems.tibemsDestination_Destroy(destination)
	if status:
		print 'Error destroying destination: ' + str(status)
		return False

	status = constants.libtibems.tibemsConnection_Close(connection)
	if status:
		print 'Error closing connection: ' + str(status)
		return False

def main():
        import os
        if not os.path.exists('data/response'):
                os.makedirs('data/response')
                
        print 'Receiving messages...'
        receiveMessages()

	import data
	symbols=data.getSymbols()
	quotes=data.getAllQuotes()
	print 'Finished loading quotes.'
	
	c=25000
	wins=0
	total=0
	
	for day in range(0, (constants.endDate-constants.startDate).days):
		currentDate=constants.startDate+datetime.timedelta(days=day)

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
			Low=quotes[best_symbol]['Low'][index]
		
			if Low<Open*0.99:
                                gain=c*.01
				c=c+2*gain
				wins=wins+1
			else:
                                loss=c-(c*Close/Open)
				c=c-2*loss
			total=total+1
		
			pwin=float(wins)/total
			print str(currentDate) + '\t' \
			+ str(round(c)) +  '\t' \
			+ best_symbol +  '\t' \
			+ str(round(best_p_vgood,5)) + '\t' \
			+ str(round(pwin,5)) + '\t'

        # make our final prediction
        ########## this is really dangerous since it could get out of sync with the test logic
	best_p_vgood=0
	best_symbol=''
        for symbol in symbols:
                date=quotes[symbol]['Date'][-1]
                filename='data/response/' + str(date) + symbol
		if os.path.exists(filename):
                        f = open(filename, 'r')
			response=cPickle.load(f)
			p=response['p']

			if p['Good']>best_p_vgood:
				best_p_vgood=p['Good']
				best_symbol=symbol

	print str(constants.endDate) + '\t' \
        + '\t' \
	+ best_symbol +  '\t' \
	+ str(round(best_p_vgood,5)) + '\t' \

main()
