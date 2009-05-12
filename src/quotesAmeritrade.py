import os
import ameritrade
import symbols
import datetime

def cleanUp():
	if os.path.exists('data/quotes'):
		import shutil
		shutil.rmtree('data/quotes')

def downloadQuotes(symbol, currentDate):
	atd = ameritrade.ameritrade()
	logIn = atd.LogIn()	

	if logIn['result'][0]!='OK':
		print 'Could not log in.'
		return
	
	year=str(currentDate.year)
	month=str(currentDate.month)
	if len(month)==1:
		month = '0' + month
	day=str(currentDate.day)
	if len(day)==1:
		day = '0' + day
	dateString = year + month + day
		
	priceHistory = atd.PriceHistory(symbol, dateString)
		
	if priceHistory:
		if not os.path.exists('data/quotes/' + symbol):
			os.makedirs('data/quotes/' + symbol)
			
		f=open('data/quotes/' + symbol + '/' + dateString + '.csv', 'w')
		for i in range(0,len(priceHistory['Open'])):
			f.write(str(priceHistory['TimeStamp'][i]) + ',' 
				   + str(priceHistory['Open'][i]) + ','
				   + str(priceHistory['High'][i]) + ','
				   + str(priceHistory['Low'][i]) + ','
				   + str(priceHistory['Close'][i]) + ','
				   + str(priceHistory['Volume'][i]) + '\n')
		f.close()
	atd.LogOut()
	return priceHistory
	
def downloadAllQuotes():
	cleanUp()
	
	symbols.downloadSymbols()
	s=symbols.getSymbols()
	
	while s:
		symbol = s.pop()
		print 'Downloading ' + symbol + '. ' + str(len(s)) + ' symbols remaining.'
		
		# Ameritrade stores 2 years of back data
		currentDate = datetime.date.today() - datetime.timedelta(days=365*2)
		endDate=datetime.date.today()
		
		while currentDate<=endDate:
			downloadQuotes(symbol, currentDate)
			currentDate = currentDate + datetime.timedelta(days=1)

def downloadQuotesForYesterday():	
	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	
	symbols.downloadSymbols()
	s=symbols.getSymbols()

	while s:
		symbol = s.pop()
		priceHistory = downloadQuotes(symbol, yesterday)
		status='failed'
		if priceHistory:
			status='succeeded'
		print 'Downloaded for ' + symbol + ' ' + status + '. ' + str(len(s)) + ' symbols remaining.'
