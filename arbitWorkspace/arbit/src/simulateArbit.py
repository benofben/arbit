import datetime
import yahoo.quotes

def getBestSymbolForDate(currentDate, quotes):
	bestSymbol=None
	bestPWin=0
	
	for symbol in quotes.keys():
		#pWin = getPWin(currentDate, quotes, symbol)
		pWin = getExpected(currentDate, quotes, symbol)
		if pWin>bestPWin:
			bestPWin=pWin
			bestSymbol=symbol
		
	return bestSymbol

def getPWin(currentDate, quotes, symbol):
	window = 30
	q = yahoo.quotes.getSubquoteForSymbolWithWindow(symbol, currentDate, quotes, window)

	if not q:
		return 0.0
	
	wins=0.0
	total = 0.0
	for i in range(0, len(q['Open'])):
		if q['High'][i]>q['Open'][i]*1.02:
			wins+=1.0
		total+=1.0
	return wins/total

def getExpected(currentDate, quotes, symbol):
	window = 100
	q = yahoo.quotes.getSubquoteForSymbolWithWindow(symbol, currentDate, quotes, window)

	if not q:
		return 0.0
	
	e=1.0
	for i in range(0, len(q['Open'])):
		if q['High'][i]>q['Open'][i]*1.02:
			e*=1.02
		else:
			e*=q['Close'][i]/q['Open'][i]
	
	return e

def simulateReturnForDate(currentDate, quotes):
	r = 1.0
	index = yahoo.quotes.getIndex(currentDate, quotes)
	
	if index:
		h = quotes['High'][index]
		o = quotes['Open'][index]
		c = quotes['Close'][index]

		if h>o*1.02:
			r = 1.02
		else:
			r = c/o
	return r

def runForDate(capital, currentDate, quotes):
	bestSymbol = None
	if currentDate.weekday()<5:
		bestSymbol = getBestSymbolForDate(currentDate, quotes)
		if bestSymbol:
			r = simulateReturnForDate(currentDate, quotes[bestSymbol])
			capital*=r
	return [capital, bestSymbol]

def run():
	capital = 25000
	#bucket = 'GOOG', 'AMZN', 'MSFT'
	#quotes = yahoo.quotes.getQuotesBucket(bucket)
	quotes = yahoo.quotes.getAllQuotes()
	
	startDate = datetime.date.today() - datetime.timedelta(days=360*3)
	endDate = datetime.date.today()
	currentDate = startDate
	
	while currentDate<endDate:
		[capital, bestSymbol] = runForDate(capital, currentDate, quotes)
		print(str(currentDate) + ',' + str(capital) + ',' + str(bestSymbol))
		currentDate = currentDate + datetime.timedelta(days=1)
		
run()
