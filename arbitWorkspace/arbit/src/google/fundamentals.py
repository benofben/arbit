import http.client
import nasdaq.symbols.downloader as symbols
import google.sql as sql
import datetime

def run(symbol, mySql, now):
	try:
		data = downloadFundamentals(symbol)
		fundamentals = parseFundamentals(data)
		fundamentals['Symbol'] = symbol
		fundamentals['Date'] = now
		mySql.insert(fundamentals)
		print('Saved fundamental data for ' + symbol + '.\n')
	except:
		print('Download of fundamental data for ' + symbol + ' failed.\n')

def downloadFundamentals(symbol):
	print('Downloading fundamental data for ' + symbol + '...')
	
	conn = http.client.HTTPConnection('www.google.com')	
	conn.request('GET', '/finance?q=' + symbol)

	response=conn.getresponse()
	print(response.status, response.reason)
	data=response.read()
	conn.close()
	if response.status==200 and response.reason=='OK':
		data = data.decode('windows-1252')
	else:
		raise Exception('Download failed for symbol ' + symbol)
	return data

def parseFundamentals(data):
	fundamentals = {}
	
	data = data.split('data-snapfield="latest_dividend-dividend_yield">Div/yield')
	data = data[1]
	temp = data.split('<td class="val">')
	temp = temp[1]
	temp = temp.split('</td>')
	fundamentals['Dividend'] = temp[0].strip()
	fundamentals['Dividend'] = fundamentals['Dividend'].split('/')
	fundamentals['Dividend'] = fundamentals['Dividend'][0]
	if fundamentals['Dividend'][-1]=='-':
		fundamentals['Dividend']=0
	fundamentals['Dividend'] = float(fundamentals['Dividend'])
		
	data = data.split('data-snapfield="eps">EPS')
	data = data[1]
	temp = data.split('<td class="val">')
	temp = temp[1]
	temp = temp.split('</td>')
	fundamentals['EPS'] = temp[0].strip()
	if fundamentals['EPS'][-1]=='-':
		fundamentals['EPS']=0
	else:
		fundamentals['EPS'] = float(fundamentals['EPS'])
		
	data = data.split('data-snapfield="shares">Shares')
	data = data[1]
	temp = data.split('<td class="val">')
	temp = temp[1]
	temp = temp.split('</td>')
	fundamentals['Shares'] = temp[0].strip()
	if fundamentals['Shares'][-1]=='-':
		fundamentals['Shares']=0
	elif fundamentals['Shares'][-1] == 'M':
		fundamentals['Shares'] = fundamentals['Shares'].replace('M', '')
		fundamentals['Shares'] = float(fundamentals['Shares'])
		fundamentals['Shares'] *= 1000000
		fundamentals['Shares'] = int(fundamentals['Shares'])
	elif fundamentals['Shares'][-1] == 'B':
		fundamentals['Shares'] = fundamentals['Shares'].replace('B', '')
		fundamentals['Shares'] = float(fundamentals['Shares'])
		fundamentals['Shares'] *= 1000000000
		fundamentals['Shares'] = int(fundamentals['Shares'])
	else:
		print('Not sure how many shares there are.' + fundamentals['Shares'])
	
	
	data = data.split('data-snapfield="inst_own">Inst. own')
	data = data[1]
	temp = data.split('<td class="val">')
	temp = temp[1]
	temp = temp.split('</td>')
	fundamentals['InstitutionalOwnership'] = temp[0].strip()
	if fundamentals['InstitutionalOwnership'][-1]=='-':
		fundamentals['InstitutionalOwnership']=0
	else:
		fundamentals['InstitutionalOwnership'] = fundamentals['InstitutionalOwnership'].replace('%','')
		fundamentals['InstitutionalOwnership'] = float(fundamentals['InstitutionalOwnership'])
		fundamentals['InstitutionalOwnership']/=100	
	
	return fundamentals

def downloadAllFundamentals():
	s = symbols.getSymbols()
	
	mySql = sql.sql()
	#mySql.drop_table()
	#mySql.create_table()

	now = datetime.datetime.now()
	
	while s:
		print(str(len(s)) + ' symbols remaining.')
		symbol = s.pop()
		symbol = symbol.replace('\n','')
		run(symbol, mySql, now)
