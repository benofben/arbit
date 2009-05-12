# Q = NASDAQ, 1 = AMEX, N = NYSE, O = OTC
exchanges=['Q', '1', 'N']

# Dictionary holds a bunch of Symbol and MarketValue
symbolDictionary={}

def downloadSymbolList(exchange):		
	print 'Trying to get exchange ' + exchange + '...'
	import httplib
	conn = httplib.HTTPConnection('www.nasdaq.com')
	conn.request('GET', '/asp/symbols.asp?exchange=' + exchange + '&start=0')
	response = conn.getresponse()
	print response.status, response.reason
	data = response.read()
	conn.close()

	print 'Done downloading.  Writing to file.\n'
	file = open('data/symbols/' + exchange + '.csv', 'w')
	file.write(data)
	file.close()

# delete the first, second and last lines from a symbols file
# the first is a header line, the last is a copyright notice
def deleteLines(filename):
	inputFile = open(filename, 'r')
	lines = inputFile.readlines()
	inputFile.close()
	
	outputFile=open(filename, 'w')
	for line in lines[2:-1]:
		outputFile.write(line)
	outputFile.close()

def writeSymbolToDictionary(symbol, marketValue):
	if marketValue != 'N/A':
		marketValue=marketValue.replace('$','')
		marketValue=marketValue.replace(',','')
		symbol=symbol.replace('^','.')
		symbolDictionary[symbol] = long(float(marketValue))*1000000

def reformatSymbolList(exchange):
	deleteLines('data/symbols/' + exchange + '.csv')
		
	filename = 'data/symbols/' + exchange + '.csv'
	inputFile = open(filename, 'rb')
	import csv
	reader = csv.reader(inputFile)

	if exchange == 'Q':
		for name,symbol,securityType,sharesOutstanding,marketValue,description in reader:
			writeSymbolToDictionary(symbol, marketValue)
	elif exchange == '1' or exchange == 'N':
		for name,symbol,marketValue,description in reader:
			writeSymbolToDictionary(symbol, marketValue)
	
	inputFile.close()

def cleanUp():
	import os
	if os.path.exists('data/symbols'):
		import shutil
		shutil.rmtree('data/symbols')
	os.makedirs('data/symbols/')

def downloadSymbols():
	cleanUp()
	
	for exchange in exchanges:
		downloadSymbolList(exchange)
		reformatSymbolList(exchange)
	
	filename='data/symbols/symbols.txt'
	file = open(filename, 'w')
	
	for symbol in symbolDictionary.keys():
		# if MarketValue>$1 billion
		if symbolDictionary[symbol]>1000000000:
			file.write(symbol + '\n')
	file.close()

def getSymbols():
	symbolFilename = 'data/symbols/symbols.txt'
	symbolFile = open(symbolFilename, 'r')
	symbols = symbolFile.readlines()
	symbolFile.close()
	
	for i in range(0, len(symbols)):
		symbols[i] = symbols[i].replace('\n','')
	
	return symbols