import os
import cPickle
import time
import shutil

serverIP='10.10.10.1'
serverPort=10000

import datetime
startDate=datetime.date(2008,1,1)
endDate=datetime.date(2009,1,1)

import data
symbols=data.getSymbols()
quotes=data.getAllQuotes()
quotesVersionNumber = datetime.datetime.now()
quotesMessage=cPickle.dumps([quotesVersionNumber,quotes])
print 'Finished loading quotes.'
def makeQueueDirectories():
	if os.path.exists('data/queue/request'):
		shutil.rmtree('data/queue/request')
	os.makedirs('data/queue/request/')

	if os.path.exists('data/queue/inProgress'):
		shutil.rmtree('data/queue/inProgress')
	os.makedirs('data/queue/inProgress/')

	if os.path.exists('data/queue/response'):
		shutil.rmtree('data/queue/response')
	os.makedirs('data/queue/response/')

def getNextRequest():
	for filename in os.listdir('data/queue/request'):
		fileContents = cPickle.load(open('data/queue/request/' + filename, 'r'))
		shutil.move('data/queue/request/' + filename, 'data/queue/inProgress/' + filename)
		return cPickle.dumps(fileContents)
	return None

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
			date=startDate+datetime.timedelta(days=day)
			print 'Pickling day ' + str(date) + '.'			
			for symbol in symbols:	
				request={}
				request['QuotesVersionNumber']=quotesVersionNumber
				request['Symbol']=symbol
				request['Date']=date
		
				f = open('data/queue/request/' + str(date) + symbol, 'w')
				cPickle.dump(request, f)
				f.close()

			#wait until the consumers grab some pickles
			while len(os.listdir('data/queue/request'))>1000:
				time.sleep(5)	
		
from BaseHTTPServer import BaseHTTPRequestHandler
class GetAndPostHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path=='/queue':
			message = getNextRequest()
		elif self.path=='/quotes':
			message = quotesMessage

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

		try:
			response=cPickle.loads(form['body'].value)
		except ValueError:
			print 'I got a bad response that pickle does not like: xxx' + form['body'].value + 'xxx'
			return

		filename=str(response['Date']) + response['Symbol']
		f = open('data/queue/response/' + filename, 'w')
		cPickle.dump(response, f)
		f.close()
		os.remove('data/queue/inProgress/' + filename)
		
def run():
	makeQueueDirectories()
	picklerThread().start()
	serverThread().start()

	# wait until all the workers are done
	numberOfItems=((endDate-startDate).days+1)*len(symbols)
	while len(os.listdir('data/queue/response'))<numberOfItems:
		time.sleep(5)
	print 'All done processing.  Going to exit now.'
	exit()

run()

