import yahoo.sql
import constants
import datetime
import yahoo.quotes

def run():
	symbols = ['PCS', 'DGIT']
	
	symbols = ['PRGS', 'PEGA', 'RHT', 'FICO', 'CRM', 'INFA', 'PVSW', 'SY', 'TDC', 'ORCL', 'IBM']
	symbols = ['IBM', 'MSFT', 'GOOG', 'ORCL', 'CA', 'EMC', 'HPQ', 'INTC', 'CSCO']
	symbols = ['GS','C','MS','BAC','JPM','WFC','DB','RBS','UBS','BCS','CS']
	
	print('Loading quotes from database...')
	yahooSql = yahoo.sql.sql()
	quotes={}
	for symbol in symbols:
		quotes[symbol] = yahooSql.fetchInformationForSymbol(symbol)
	print('Done loading.')
	
	print(quotes)
	
	take = 0.005
	window = 13
	simulate(symbols, quotes, window, take)
			
def simulate(symbols, quotes, window, take):
	capital = 25000
	
	currentDate = constants.startDate
	while currentDate < constants.endDate:
		[symbol, pWin] = getBestSymbol(symbols, quotes, window, currentDate)
		if symbol:
			capital *= getReturn(symbol, currentDate, quotes, take)
			print(currentDate.isoformat() + '\t' + str(capital) + '\t' + symbol + '\t' + str(pWin))
		currentDate = currentDate + datetime.timedelta(days=1)
	return capital

def getBestSymbol(symbols, quotes, window, currentDate):
	bestPWin=0
	bestSymbol=None
	
	for symbol in symbols:
		pWin  = getPWinForSymbol(quotes[symbol], window, currentDate)
		if pWin>bestPWin:
			bestPWin=pWin
			bestSymbol=symbol
	
	return [bestSymbol, bestPWin]

def getPWinForSymbol(quotes, window, currentDate):
	i = yahoo.quotes.getIndex(currentDate, quotes)
	
	if not i:
		# we don't have any data
		return 0
	
	if i-window < 0:
		# we don't have enough data
		return 0

	pWin=0
	total=0
	for j in range(i-window, i):
		total=total+1
		if quotes['High'][j]>quotes['Open'][j]*1.02:
			pWin=pWin+1
	
	pWin=pWin/total
	return pWin
	
def getMax(p):
	b = dict(map(lambda item: (item[1],item[0]),p.items()))
	return b[max(b.keys())]

def getReturn(bestSymbol, currentTestDate, quotes, take):
	i = yahoo.quotes.getIndex(currentTestDate, quotes[bestSymbol])
	
	if not i:
		return 1
	elif quotes[bestSymbol]['High'][i]>quotes[bestSymbol]['Open'][i]*(1+take):
		return 1+take
	else:
		return quotes[bestSymbol]['Close'][i]/quotes[bestSymbol]['Open'][i]

run()