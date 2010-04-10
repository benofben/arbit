import os
import ameritrade
import symbols
import datetime
import csv
import constants

def __downloadQuotes(symbol, currentDate, atd):
	if currentDate.weekday()==5 or currentDate.weekday()==6:
		return 'weekend'
	
	year=str(currentDate.year)
	month=str(currentDate.month)
	if len(month)==1:
		month = '0' + month
	day=str(currentDate.day)
	if len(day)==1:
		day = '0' + day
	dateString = year + month + day
	
	# This is hideous, but I've been having filesystem issues.
	sanitizedSymbol=symbol.replace('^','c')
	sanitizedSymbol=sanitizedSymbol.replace('/','s')
	filename = constants.dataDirectory + 'ameritrade/quotes/' + sanitizedSymbol + '/' + dateString + '.csv'
	if os.path.exists(filename):
		return 'exists'
	
	priceHistory = atd.PriceHistory(symbol, dateString)
	
	if not priceHistory:
		return 'failed'
	
	if priceHistory:
		if not os.path.exists(constants.dataDirectory + 'ameritrade/quotes/' + sanitizedSymbol):
			os.makedirs(constants.dataDirectory + 'ameritrade/quotes/' + sanitizedSymbol)
		
		f=open(filename, 'w')
		for i in range(0,len(priceHistory['Open'])):
			f.write(str(priceHistory['TimeStamp'][i]) + ',' 
				   + str(priceHistory['Open'][i]) + ','
				   + str(priceHistory['High'][i]) + ','
				   + str(priceHistory['Low'][i]) + ','
				   + str(priceHistory['Close'][i]) + ','
				   + str(priceHistory['Volume'][i]) + '\n')
		f.close()
	
	return priceHistory

# Downloads symbols from endDate to startDate inclusive.
def downloadAllQuotes(startDate, endDate):
	symbols.downloadSymbols()
	s=symbols.getSymbols()
	
	atd = ameritrade.ameritrade()
	logIn = atd.LogIn()	
	
	if not logIn or logIn['result'][0]!='OK':
		print ('Could not log in.')
		return 'failed'
	
	currentDate = endDate
	while currentDate >= startDate:
		for symbol in s:
			priceHistory = __downloadQuotes(symbol, currentDate, atd)
			
			if priceHistory == 'weekend':
				status=priceHistory
			elif priceHistory == 'exists':
				status=priceHistory
				print ('Download for ' + symbol + ' on ' + currentDate.isoformat() + ' ' + status + '.')
			elif priceHistory == 'failed':
				status=priceHistory
				print ('Download for ' + symbol + ' on ' + currentDate.isoformat() + ' ' + status + '.')
			else:
				status='succeeded'
				print ('Download for ' + symbol + ' on ' + currentDate.isoformat() + ' ' + status + '.')
			
		currentDate = currentDate - datetime.timedelta(days=1)
		
	atd.LogOut()

def downloadEverything():
	# Ameritrade stores 2 years of back data, but starts at the 1st of the month
	startDate = datetime.date.today() - datetime.timedelta(days=365*2)
	startDate = startDate.replace(day=1)
	endDate=datetime.date.today() - datetime.timedelta(days=1)
	downloadAllQuotes(startDate, endDate)

def getAllQuotes(startDate, endDate):
	quotes = {}
	for symbol in os.listdir(constants.dataDirectory + 'ameritrade/pruned'):
		quotes[symbol]=__getQuotes(symbol, startDate, endDate)
		print ('Loaded ' + symbol)
	return quotes

def __getQuotes(symbol, startDate, endDate):
	a=[]
	currentDate = endDate
	while currentDate >= startDate:
		year=str(currentDate.year)
		month=str(currentDate.month)
		if len(month)==1:
			month = '0' + month
		day=str(currentDate.day)
		if len(day)==1:
			day = '0' + day
		dateString = year + month + day
		
		filename = constants.dataDirectory + 'ameritrade/pruned/' + symbol + '/' + dateString + '.csv'
		
		try:
			file = open(filename, 'r')
			reader = csv.reader(file)
			b={}
			b['TimeStamp']=[]
			b['Open']=[]
			b['High']=[]
			b['Low']=[]
			b['Close']=[]
			b['Volume']=[]
			
			for TimeStamp, Open, High, Low, Close, Volume in reader:
				b['TimeStamp'].append(datetime.datetime.fromtimestamp(int(TimeStamp) / 1000))
				b['Open'].append(float(Open))
				b['High'].append(float(High))
				b['Low'].append(float(Low))
				b['Close'].append(float(Close))
				b['Volume'].append(int(Volume))
			file.close()
			a.append(b)
		except IOError:
			pass
		
		currentDate = currentDate - datetime.timedelta(days=1)
	
	return a
