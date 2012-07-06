import yahoo.sql
import constants
import datetime
import yahoo.quotes

def run():
	print('Loading quotes from database...')
	yahooSql = yahoo.sql.sql()
	q = yahooSql.fetchInformation()
	symbols = getUniqueList(q['Symbol'])
	q = reformatQuotes(q, symbols)
	print('Done loading.')
	
	file = open('C:\\w.txt', 'w')
	file.close()
	
	for window in range(1,5000):
		capital = simulateForWindow(window, symbols, q)
		file = open('C:\\w.txt', 'a')
		file.write(str(window) + ',' + str(capital) + '\n')
		file.close()
		print(str(window) + ',' + str(capital))

def simulateForWindow(window, symbols, quotes):
	currentTestDate = constants.startDate
	capital = 25000
	while currentTestDate < constants.endDate:
		currentTrainingDate = currentTestDate - datetime.timedelta(days=1)

		p={}
		for symbol in symbols:			
			p[symbol] = pWin(window, quotes[symbol], currentTrainingDate)
		bestSymbol = getMax(p)
		
		capital *= getReturn(bestSymbol, currentTestDate, quotes)
		currentTestDate = currentTestDate + datetime.timedelta(days=1)

	return capital

def getUniqueList(list):
	# element order preserved
	set = {}
	return [ set.setdefault(x,x) for x in list if x not in set ]

def pWin(window, quotes, currentTrainingDate):
	i = yahoo.quotes.getIndex(currentTrainingDate, quotes)
	
	if not i:
		# we don't have any data
		return 0
	
	if i-window < 0:
		# we don't have enough data
		return 0
	
	p=0
	total=0
	for j in range(i+1-window, i+1):
		total=total+1
		if quotes['High'][j]>quotes['Open'][j]*1.02:
			p=p+1
	
	p=p/total
	return p

def getMax(p):
	b = dict(map(lambda item: (item[1],item[0]),p.items()))
	return b[max(b.keys())]

def getReturn(bestSymbol, currentTestDate, quotes):
	i = yahoo.quotes.getIndex(currentTestDate, quotes[bestSymbol])
	
	if not i:
		return 1
	elif quotes[bestSymbol]['High'][i]>quotes[bestSymbol]['Open'][i]*1.02:
		return 1.02
	else:
		return quotes[bestSymbol]['Close'][i]/quotes[bestSymbol]['Open'][i]
	
def reformatQuotes(q, symbols):
	newQ = {}
	for symbol in symbols:
		newQ[symbol]={}
		for key in q:
			if key != 'Symbol':
				newQ[symbol][key]=[]
		
	for i in range(0, len(q['Symbol'])):
		symbol=q['Symbol'][i]
		
		for key in q:
			if key != 'Symbol':
				newQ[symbol][key].append(q[key][i])
			
	return newQ

run()