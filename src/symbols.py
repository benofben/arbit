import constants

# Options are: NYSE, NASDAQ, AMEX
exchanges=['NYSE', 'NASDAQ', 'AMEX']

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
	
	# The download files have broken line endings.  This seems to be working on Windows and will probably cause horrible disasters if this is run on Linux.
	data = data.decode('windows-1252')
	data = data.replace(',\r','')
	
	file.write(data)
	file.close()

def downloadSymbols():
	import os
	if os.path.exists(constants.dataDirectory + 'symbols'):
		import shutil
		shutil.rmtree(constants.dataDirectory + 'symbols')
	os.makedirs(constants.dataDirectory + 'symbols')
	
	for exchange in exchanges:
		downloadSymbolList(exchange)

def getSymbolInformationForExchange(exchange):
	symbolInformation = {}
	inputFile = open(constants.dataDirectory + 'symbols/' + exchange + '.csv', 'r')
	import csv
	reader = csv.reader(inputFile)
	import re
	for Symbol, unused_Name, unused_LastSale, MarketCap, IPOyear, Sector, Industry, unused_SummaryQuote in reader:
		if(Symbol == 'Symbol'):
			# Then this is the first line
			pass
		else:
			#remove whitespace from end of symbol
			Symbol = re.sub(r'\s', '', Symbol)
			symbolInformation[Symbol]={}
			symbolInformation[Symbol]['Exchange']=exchange
			symbolInformation[Symbol]['MarketCap']=float(MarketCap)
			symbolInformation[Symbol]['IPOYear']=IPOyear
			symbolInformation[Symbol]['Sector']=Sector
			symbolInformation[Symbol]['Industry']=Industry
	
	inputFile.close()
	
	return symbolInformation
	
def getSymbolInformation():
	symbolInformation = {}
	for exchange in exchanges:
		dict = getSymbolInformationForExchange(exchange)
		# copy the dictionary for one exchange to the aggregated dictionary
		for key in dict.keys(): 
			symbolInformation[key]=dict[key]
			
	return symbolInformation

def getSymbols():
	symbolInformation = getSymbolInformation()
	symbols = []
	for symbol in symbolInformation:
		symbol = symbol.replace('/', '')
		symbols.append(symbol)
	return symbols