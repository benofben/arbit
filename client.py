import cPickle
import httplib
import validators
import socket
import time

serverIP='10.97.153.33'
serverPort=8123

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

def send(data):
    pickledData = cPickle.dumps(data)
    try:
        conn = httplib.HTTPConnection(serverIP, serverPort)
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        conn.request('POST', '/', 'body=' + pickledData, headers)
        response = conn.getresponse()
        conn.close()
    except socket.error:
        print 'socket error: Could not send response.'
        return
    if response.status!=200 or response.reason!='OK':
        print 'Could not send response.'
        print response.status, response.reason

def run():
    while(True):
        quotes=receive()
        if quotes:
            print 'Processing ' + quotes['Symbol'] + ' for day ' + str(quotes['Date'][-1]) + '.'
            response = validators.EvaluateQuotes(quotes)
            response['Symbol']=quotes['Symbol']
            response['TargetDate']=quotes['TargetDate']
            send(response)
        else:
            time.sleep(5)

run()
