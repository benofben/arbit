import os
import cPickle
import time

import data
symbols=data.getSymbols()
quotes=data.getAllQuotes()

import datetime
startDate=datetime.date(2003,1,1)
endDate=datetime.date.today()

def makeQueueDirectories():
    import shutil
    
    if os.path.exists('data/request'):
        shutil.rmtree('data/request')
    os.makedirs('data/request/')

    if os.path.exists('data/response'):
        shutil.rmtree('data/response')
    os.makedirs('data/response/')

def getNumberOfItems():
    numberOfItems=0
    for day in range(0, (endDate-startDate).days+1):
        for symbol in symbols:
            i=data.getIndex(startDate+datetime.timedelta(days=day), quotes[symbol])
            if i:
                numberOfItems=numberOfItems+1
    return numberOfItems

def getNextRequest():
    for filename in os.listdir('data/request'):
        fileContents = cPickle.load(open('data/request/' + filename, 'r'))
        os.remove('data/request/' + filename)
        return cPickle.dumps(fileContents)
    return None

from threading import Thread
class serverThread(Thread):
    def __init__ (self):
        Thread.__init__(self)
        self.status = -1
    def run(self):
        from BaseHTTPServer import HTTPServer
        server = HTTPServer(('localhost', 8000), GetAndPostHandler)
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
                    index[symbol]=i

            for symbol in index:
                subQuotes=data.getQuotesSubset(index, symbol, quotes)
                f = open('data/request/' + str(startDate+datetime.timedelta(days=day)) + symbol, 'w')
                subQuotes['TargetDate']=startDate+datetime.timedelta(days=day)
                cPickle.dump(subQuotes, f)
                f.close()

            #wait until the consumers grab some pickles
            while len(os.listdir('data/request'))>100:
                time.sleep(60)
    
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
        f = open('data/response/' + str(response['TargetDate']) + response['Symbol'], 'w')
        cPickle.dump(response, f)
        f.close()

def run():
    makeQueueDirectories()
    serverThread().start()
    picklerThread().start()

    # wait until all the workers are done
    numberOfItems=getNumberOfItems()
    while len(os.listdir('data/response'))<numberOfItems:
        time.sleep(60)
    exit()

run()
