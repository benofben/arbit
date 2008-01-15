import os
import cPickle
import time
import shutil

serverIP='localhost'
serverPort=8123

import data
symbols=data.getSymbols()
quotes=data.getAllQuotes()

import datetime
startDate=datetime.date(2007,1,1)
endDate=datetime.date.today()

from threading import Thread
class serverThread(Thread):
    def __init__ (self):
        Thread.__init__(self)
        self.status = -1
    def run(self):
        from BaseHTTPServer import HTTPServer
        server = HTTPServer((serverIP, serverPort), GetAndPostHandler)
        print 'Starting http server...'
        server.serve_forever()

class picklerThread(Thread):
    def __init__ (self):
        Thread.__init__(self)
        self.status = -1
    def run(self):
        for day in range(0, (endDate-startDate).days+1):
            print 'Pickling day ' + str(startDate+datetime.timedelta(days=day)) + '.'

            index={}
            for symbol in symbols:
                i=data.getIndex(startDate+datetime.timedelta(days=day), quotes[symbol])
                if i:
                    if quotes[symbol]['Volume'][i]>500000:
                        index[symbol]=i

            for symbol in index:
                subQuotes=data.getQuotesSubset(index, symbol, quotes, 242)
                if subQuotes:
                    f=open('data/queue/request/' + str(subQuotes['Date'][-1]) + symbol, 'w')
                    cPickle.dump(subQuotes, f)
                    f.close()

            #wait until the consumers grab some pickles
            while len(os.listdir('data/queue/request'))>100:
                time.sleep(60)

def getNextRequest():
    for filename in os.listdir('data/queue/request'):
        fileContents = cPickle.load(open('data/queue/request/' + filename, 'r'))
        shutil.move('data/queue/request/' + filename, 'data/queue/inProgress/' + filename)
        return cPickle.dumps(fileContents)
    return None
    
from BaseHTTPServer import BaseHTTPRequestHandler
class GetAndPostHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = getNextRequest()

        if message:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(message)
        else:
            self.send_response(500)
            self.end_headers()

    def do_POST(self):
        import cgi
        form=cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        self.send_response(200)
        self.end_headers()

        response=cPickle.loads(form['body'].value)
        filename=str(response['Date']) + response['Symbol']
        f = open('data/queue/response/' + filename, 'w')
        cPickle.dump(response, f)
        f.close()
        os.remove('data/queue/inProgress/' + filename)

def makeQueueDirectories():
    if os.path.exists('data/queue/request'):
        shutil.rmtree('data/queue/request')
    os.makedirs('data/queue/request/')
    if os.path.exists('data/queue/inProgress'):
        shutil.rmtree('data/queue/inProgress')
    os.makedirs('data/queue/inProgress/')
    if not os.path.exists('data/queue/response'):
        os.makedirs('data/queue/response/')

def run():
    makeQueueDirectories()
    serverThread().start()
    picklerThread().start()

    while True:
        time.sleep(60)

run()
