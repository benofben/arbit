import cPickle
import httplib
import validators
import socket

serverIP='10.97.153.33'
serverPort=8123

def send(response):
    pickledResponse = cPickle.dumps(response)
    try:
        conn = httplib.HTTPConnection(serverIP, serverPort)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn.request('POST', '/', 'body=' + pickledResponse, headers)
        response = conn.getresponse()
        conn.close()
    except socket.error:
        print 'socket error: Could not send response.'
        return
    
    if response.status!=200 or response.reason!='OK':
        print 'Could not send response.'
        print response.status, response.reason
    

def receive():
    try:
        conn = httplib.HTTPConnection(serverIP, serverPort)
        conn.request('GET', '/')
        response=conn.getresponse()
        pickledData=response.read()
        conn.close()
    except socket.error:
        return None
    except httplib.BadStatusLine:
	return None
    if response.status!=200 or response.reason!='OK':
        return None

    return cPickle.loads(pickledData)

def run():
    while(True):
        quotes=receive()
        if quotes:
            print "Processing " + quotes['Symbol'] + ' for day ' + str(quotes['Date'][-1]) +'.'
            response = validators.FindWindow(quotes)
            response['Symbol']=quotes['Symbol']
            response['Date']=quotes['Date'][-1]
            send(response)
        else:
            import time
            time.sleep(5)

run()
