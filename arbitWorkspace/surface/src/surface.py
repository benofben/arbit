# Want to compute a surface for pWin
# Data points look like
# Pwin(t+1), Pwin(window), window

import yahooSql
import surfaceSql
from datetime import date
from datetime import timedelta

def run():
	myYahooSql = yahooSql.sql()
	mySurfaceSql = surfaceSql.sql()
	mySurfaceSql.drop_table()
	mySurfaceSql.create_table()

	startDate = date.today() - timedelta(days=300)
	endDate = date.today()

	symbols = myYahooSql.fetchSymbols(startDate, endDate)
	data={}
	for symbol in symbols:
		data[symbol] = myYahooSql.fetchOpenHigh(symbol, startDate, endDate)
	print('Done loading data.')	

	for window in range(1,1000):
		print('Working on window ' + str(window))
		points = {}
		for symbol in data:
			for i in range(window, len(data[symbol]['Open'])):
				[pWin, outcome] = computePoint(data[symbol], window, i)
				
				key = str(window)+str(pWin)
				if key in points:
					points[key]['Wins']=points[key]['Wins']+outcome
					points[key]['Total']=points[key]['Total']+1
				else:
					points[key]={}
					points[key]['Window']=window
					points[key]['Pwin']=pWin
					points[key]['Wins']=outcome
					points[key]['Total']=1
		
		for key in points:
			points[key]['Outcome']=points[key]['Wins']/points[key]['Total']	
		mySurfaceSql.insert(points)

def computePoint(data, window, i):
	total = 0
	pWin = 0
	
	for j in range(i-window, i):
		if data['High'][j]>data['Open'][j]*1.02:
				pWin = pWin + 1
		total = total + 1
	pWin = pWin / total
			
	if data['High'][i]>data['Open'][i]*1.02:
		outcome = 1
	else:
		outcome = 0
	
	return [pWin, outcome]

run()