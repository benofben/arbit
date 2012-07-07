import constants
import datetime
import nasdaq.downloader as symbols
import yahoo.sql as sql

def downloadQuotes(symbol):
	print('Downloading historical data for ' + symbol + '...')
	import http.client
	conn = http.client.HTTPConnection('ichart.finance.yahoo.com')
	
	'''
	Notes on the yahoo parameters:
	d=end month-1 
	e=end day
	f=end year
	g=d?
	a=start month-1 (0 = January)
	b=start day (2)
	c=start year (2002)
	'''
	
	today = datetime.date.today()
	endYear = today.strftime('%Y')
	endMonth = str(int(today.strftime('%m'))-1)
	endDay = today.strftime('%d')
	
	startYear='2002'
	startMonth='0'
	startDay='1'
	
	conn.request('GET', '/table.csv?s=' + symbol + '&d=' + endMonth + '&e=' + endDay + '&f=' + endYear + '&g=d&a=' + startMonth + '&b=' + startDay + '&c=' + startYear + '&ignore=.csvc')
	response=conn.getresponse()
	print(response.status, response.reason)
	data=response.read()
	conn.close()
	if response.status==200 and response.reason=='OK':
		data = data.decode('windows-1252')
		reformatAndSaveQuotes(data, symbol)
		print('Saved historical data for ' + symbol + '.\n')
	else:
		print('Download failed for symbol ' + symbol + '.\n')
		return False
	return True

def reformatAndSaveQuotes(data, symbol):
	quotes=[]
	lines = data.split('\n')
	i=0
	for line in lines:
		if(i>0):
			quotes.append(line)
		i=i+1
	
	# we want the list to go from oldest quote to newest
	quotes.reverse()

	filename=constants.dataDirectory + 'yahoo/quotes/' + symbol + '.csv'
	file=open(filename, 'w')
	i=0
	for line in quotes:
		if(i>0):
			file.write(line + '\n')
		i=i+1
	file.close()

def cleanUp():
	import os
	if os.path.exists(constants.dataDirectory + 'yahoo/quotes'):
		import shutil
		shutil.rmtree(constants.dataDirectory + 'yahoo/quotes')
	os.makedirs(constants.dataDirectory + 'yahoo/quotes/')

def downloadAllQuotes():
	cleanUp()
	s = symbols.getSymbols()
	
	failedSymbolsFilename = constants.dataDirectory + 'yahoo/failedQuotesSymbols.txt'
	failedSymbolsFile = open(failedSymbolsFilename, 'w')
	
	mySql = sql.sql()
	mySql.drop_table()
	mySql.create_table()

	while s:
		print(str(len(s)) + ' symbols remaining.')
		symbol = s.pop()
		symbol = symbol.replace('\n','')
		if not downloadQuotes(symbol):
			failedSymbolsFile.write(symbol + '\n')
		else:
			quotes = getQuotes(symbol)
			quotes['Symbol'] = symbol
			mySql.insert(quotes)
			
	failedSymbolsFile.close()

#############################################################
### For loading the data set once it has been downloaded. ###
#############################################################

def getQuotes(symbol):
	inputFilename=constants.dataDirectory + 'yahoo/quotes/' + symbol + '.csv'
	inputFile=open(inputFilename, 'r')

	quotes={}
	quotes['Date']=[]
	quotes['Open']=[]
	quotes['High']=[]
	quotes['Low']=[]
	quotes['Close']=[]
	quotes['Volume']=[]
	quotes['AdjClose']=[]
	
	import csv
	reader=csv.reader(inputFile)
	
	for Date, Open, High, Low, Close, Volume, AdjClose in reader:
		dt=Date.split('-')
		Date=datetime.date(int(dt[0]), int(dt[1]), int(dt[2]))
		
		quotes['Date'].append(Date)
		quotes['Open'].append(float(Open))
		quotes['High'].append(float(High))
		quotes['Low'].append(float(Low))
		quotes['Close'].append(float(Close))
		quotes['Volume'].append(int(Volume))
		quotes['AdjClose'].append(float(AdjClose))
	
	inputFile.close()
	return quotes

# returns the index of the quote for the given date for quotes[symbol]
def getIndex(date, quotes):
	try:
		return quotes['Date'].index(date)
	except ValueError:
		return False
	
def getUniqueList(list):
	# element order preserved
	set = {}
	return [ set.setdefault(x,x) for x in list if x not in set ]

def reformatQuotes(q, symbols):
	newQ = {}
	for symbol in symbols:
		newQ[symbol]={}
		for key in q:
			if key != 'Symbol':
				newQ[symbol][key]=[]
		
	for i in range(0, len(q['Symbol'])):
		symbol=q['Symbol'][i]
		
		for key in q:
			if key != 'Symbol':
				newQ[symbol][key].append(q[key][i])
			
	return newQ
