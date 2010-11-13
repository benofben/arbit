import constants

# Options are: NYSE, NASDAQ, AMEX
exchanges=['NYSE', 'NASDAQ']
symbols=[]

def downloadSymbolList(exchange):
	print('Trying to get exchange ' + exchange + '...')
	import http.client
	conn = http.client.HTTPConnection('www.nasdaq.com')
	conn.request('GET', '/screening/companies-by-industry.aspx?exchange=' + exchange + '&render=download')
	response = conn.getresponse()
	print(response.status, response.reason)
	data = response.read()
	conn.close()
	
	print('Done downloading.  Writing to file.\n')
	file = open(constants.dataDirectory + 'symbols/' + exchange + '.csv', 'w')
	
	# The download files have broken line endings.  This seems to be working on Windows and will probably
	# cause horrible disasters if this is run on Linux.
	data = data.decode('windows-1252')
	data = data.replace(',\r','')
	
	file.write(data)
	file.close()

# delete the first line, a header line, from a symbols file
def deleteLines(filename):
	inputFile = open(filename, 'r')
	lines = inputFile.readlines()
	inputFile.close()
	
	outputFile=open(filename, 'w')
	for line in lines[1:]:
		outputFile.write(line)
	outputFile.close()

def reformatSymbolList(exchange):
	deleteLines(constants.dataDirectory + 'symbols/' + exchange + '.csv')
	
	filename = constants.dataDirectory + 'symbols/' + exchange + '.csv'
	inputFile = open(filename, 'r', newline='')
	import csv
	reader = csv.reader(inputFile)

	for symbol, name, lastSale, marketCap, iPOYear, sector, industry, summaryQuote in reader:
		if float(marketCap)>10.0**9:
			symbols.append(symbol)
		
	inputFile.close()

def downloadSymbols():
	import os
	if os.path.exists(constants.dataDirectory + 'symbols'):
		import shutil
		shutil.rmtree(constants.dataDirectory + 'symbols')
	os.makedirs(constants.dataDirectory + 'symbols/')
	
	for exchange in exchanges:
		downloadSymbolList(exchange)
		reformatSymbolList(exchange)
	
	filename=constants.dataDirectory + 'symbols/symbols.txt'
	file = open(filename, 'w')
	
	import re
	for symbol in symbols:
		#remove whitespace from end of symbol
		symbol = re.sub(r'\s', '', symbol)
		file.write(symbol + '\n')
	file.close()

def getSymbols():
	symbolFilename = constants.dataDirectory + 'symbols/symbols.txt'
	symbolFile = open(symbolFilename, 'r')
	symbols = symbolFile.readlines()
	symbolFile.close()
	
	for i in range(0, len(symbols)):
		symbols[i] = symbols[i].replace('\n','')
	
	return symbols
