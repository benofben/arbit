def getNextPickledSubQuotes():
    return 'hi'

from BaseHTTPServer import BaseHTTPRequestHandler
class GetAndPostHandler(BaseHTTPRequestHandler):
    
    # a node has asked for some work to do.
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        message = getNextPickledSubQuotes()
        self.wfile.write(message)
        return

    # a node is sending back its finished work.
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()

        self.wfile.write('Client: %s\n' % str(self.client_address))
        self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write('Form data:\n')

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                self.wfile.write('\tUploaded %s (%d bytes)\n' % (field, file_len))
            else:
                # Regular form value
                self.wfile.write('\t%s=%s\n' % (field, form[field].value))
        return

# now let's run the master
capital=25000
    
import data
symbols=data.getSymbols()
quotes=data.getAllQuotes()

import datetime
startDate=datetime.date(2003,1,1)
endDate=datetime.date.today()

# start the HTTP server
from BaseHTTPServer import HTTPServer
server = HTTPServer(('localhost', 8000), GetAndPostHandler)
print 'Starting http server...'
server.serve_forever()

# now we simulate for each day
for day in range(0, (endDate-startDate).days):
    
    index={}
    for symbol in symbols:
        i=data.getIndex(startDate+datetime.timedelta(days=day), quotes[symbol])
        if i:
            index[symbol]=i

    for symbol in index:
        subQuotes=data.getQuotesSubset(index, symbol, quotes)
        pickledSubQuotes = cPickle.dumps(subQuotes)
