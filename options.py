def downloadOptionsData(symbol, date):
	print 'Downloading option data for ' + symbol + '...'
	import httplib
	conn = httplib.HTTPConnection('finance.yahoo.com')
	
	conn.request('GET', '/q/os?s=' + symbol+ '&m=' + date)
	response=conn.getresponse()
	print response.status, response.reason
	data=response.read()
	conn.close()
	if response.status==200 and response.reason=='OK':
		reformatAndSaveOptionsData(data, symbol, date)
		print 'Saved options data for ' + symbol + '.\n'
	else:
		print 'Option data download failed for symbol ' + symbol + '.\n'
		return False
	return True

def parseData(data):
	import re
	
	try:
		# get the right section of the html
		m = re.search('Options Expiring[\s\S]*Return to Stacked View', data)
		data=m.group(0)
	
		# get the table
		m = re.search('yfnc_tablehead1_c[\s\S]*?</table>', data)
		data=m.group(0)
	
		# strip off the first row
		m = re.search('Open Int</td></tr><tr>[\s\S]*', data)
		data=m.group(0)
	
		# strip off a little more
		m = re.search('yfnc_h[\s\S]*', data)
		data=m.group(0)
	
		m = re.split('<td', data)
		rows=len(m)/15
		
		options=[]
		for rowIndex in range(0,rows):
			for columnIndex in range(0,15):
				i = rowIndex*15+columnIndex
				m[i] = re.search('>[\s\S]*?</', m[i]).group(0)
				m[i] = re.sub('[\s\S]*>', '', m[i])
				m[i] = re.sub('</', '', m[i])
				m[i] = re.sub(',', '', m[i])
				
			# 0-6 are the call
			# 7 is the strike
			# 8-14 are the put
				
			row=[]
			row.append(m[0])
			row.append(m[1])
			row.append(m[2])
			row.append(m[3])
			row.append(m[4])
			row.append(m[5])
			row.append(m[6])
			row.append(m[7])
			row.append('C')
			options.append(row)
			
			row=[]
			row.append(m[8])
			row.append(m[9])
			row.append(m[10])
			row.append(m[11])
			row.append(m[12])
			row.append(m[13])
			row.append(m[14])
			row.append(m[7])
			row.append('P')
			options.append(row)
	
	except AttributeError:
		print 'There was no option data in the html file.'
		return	None
	
	return options
	
def reformatAndSaveOptionsData(data, symbol, date):
	options = parseData(data)
	if not options:
		return
	
	filename='data/options/' + symbol + date + '.csv'
	file=open(filename, 'w')
	
	import csv
	dialect=csv.excel
	dialect.lineterminator='\n'
	csvwriter = csv.writer(file, delimiter=',', dialect=dialect)
	csvwriter.writerows(options)
	
	file.close()
	
def downloadAllOptionsData():
	import datetime
	
	import os
	if not os.path.exists('data/options'):
		os.makedirs('data/options/')
	
	symbolFilename = 'data/symbols/symbols.txt'
	symbolFile = open(symbolFilename, 'r')
	symbols = symbolFile.readlines()
	symbolFile.close()

	failedSymbolsFilename = 'data/symbols/failedOptionsSymbols.txt'
	failedSymbolsFile = open(failedSymbolsFilename, 'w')

	while symbols:
		print str(len(symbols)) + ' symbols remaining.'
		symbol = symbols.pop()
		symbol = symbol.replace('\n','')
		
		for i in range(0,11):
			today = datetime.date.today()
			endYear = int(today.strftime('%Y'))
			endMonth = int(today.strftime('%m'))+i
			if endMonth>12:
				endMonth=endMonth%12
				endYear=endYear+1
			date = str(endYear) + '-' + str(endMonth)
			
			if not downloadOptionsData(symbol, date):
				failedSymbolsFile.write(symbol + '\n')

	failedSymbolsFile.close()
