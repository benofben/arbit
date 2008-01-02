import cPickle
import time
import validators
import httplib

def send(quotes):
    pickledQuotes = cPickle.dumps(quotes)
    conn = httplib.HTTPConnection('localhost', 8161)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn.request('POST', '/demo/message/FOO/BAR', 'destination=response&type=queue&body=' + pickledQuotes, headers)
    response = conn.getresponse()
    if response.status!=200 or response.reason!='OK':
        print 'Could not send message to queue.'
        print response.status, response.reason

    data = response.read()
    conn.close()

def receive():
    conn = httplib.HTTPConnection('localhost', 8161)
    conn.request('GET', '/demo/message/request?timeout=10000&type=queue')
    response=conn.getresponse()
    pickledData=response.read()
    conn.close()

    if response.status!=200 or response.reason!='OK':
        print 'Could not get a message from queue.  Will try again in 5 seconds.'
        time.sleep(5)
        return False

    return cPickle.dumps(pickledData)

def run():
    while(True):
        quotes=receive()
        if quotes:
            print "Processing "
            print quotes
            #response = validators.FindWindow(quotes)
            #response['Symbol']=quotes['Symbol']
            #pickledResponse = cPickle.dumps(response)
            #send(pickledResponse)

run()
