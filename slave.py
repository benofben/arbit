import cPickle
import validators
import time
import sys
import stomp

class MyListener(object):
    def on_error(self, headers, message):
        print 'received an error %s' % message
        
    def on_message(self, headers, message):
        quotes = cPickle.loads(message)
        response = validators.FindWindow(quotes)
        response['Symbol']=quotes['Symbol']
        conn.send(cPickle.dumps(response), destination='/queue/response')
        
def run():
    conn = stomp.Connection()
    conn.add_listener(MyListener())
    conn.start()
    conn.connect()
    conn.subscribe(destination='/queue/request', ack='auto')
    while(True):
        time.sleep(1)
    conn.disconnect()

run()
