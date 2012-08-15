import constants
import datetime
import briefing.sql
import yahoo.sql

def simulate():
	upgradeSql = briefing.sql.sql()
	quoteSql = yahoo.sql.sql()
	
	capital = 10000
	
	currentDate = constants.startDate
	while currentDate<constants.endDate:
		[capital, symbols] = simulateForDate(currentDate, capital, upgradeSql, quoteSql)
		print(currentDate.isoformat() + '\t' + str(currentDate.isoweekday()) +'\t$' + str(capital) + '\t' + str(symbols))
		currentDate = currentDate + datetime.timedelta(days=1)

def simulateForDate(currentDate, capital, upgradeSql, quoteSql):
	upgrades = upgradeSql.fetch(currentDate - datetime.timedelta(days=1), 'Upgrade')
	symbols=[]
	
	# Check if there are upgrades to trade on today.
	if(not upgrades):
		return [capital, symbols]
	
	for upgrade in upgrades:
		r = calculateReturnForDate(upgrade['Ticker'], currentDate, quoteSql)
		if r!=0:
			symbols.append([upgrade['Ticker'], r])
	
	leverage = 3
	if len(symbols)>0:
		capitalPerTrade = (capital*leverage)/len(symbols)
		for [unused_ticker, r] in symbols:
			capital = capital + capitalPerTrade * r
		capital = round(capital, 2)
	
	return [capital, symbols]

def calculateReturnForDate(symbol, currentDate, quoteSql):
	analystQuote = quoteSql.fetchForSymbolAndDate(symbol, currentDate - datetime.timedelta(days=1))
	quote = quoteSql.fetchForSymbolAndDate(symbol, currentDate)
	trailingQuote = quoteSql.fetchForSymbolAndDate(symbol, currentDate + datetime.timedelta(days=3))

	r = 0
	
	if not quote or not analystQuote or not trailingQuote:
		pass
	else:
		
		# Check if the stock has jumped too much to buy
		if analystQuote['Close']*0.99>quote['Open']:
		
			buyPrice = quote['Open']
			sellPrice = trailingQuote['Close']
			delta = buyPrice-sellPrice
			r = delta/buyPrice

	return r


'''
this is doing reasonably well. +3k over 4 months.
def calculateReturnForDate(symbol, currentDate, quoteSql):
	analystQuote = quoteSql.fetchForSymbolAndDate(symbol, currentDate - datetime.timedelta(days=1))
	quote = quoteSql.fetchForSymbolAndDate(symbol, currentDate)
	trailingQuote = quoteSql.fetchForSymbolAndDate(symbol, currentDate + datetime.timedelta(days=3))

	r = 0
	
	if not quote or not analystQuote or not trailingQuote:
		pass
	else:
		
		# Check if the stock has jumped too much to buy
		if analystQuote['Close']*0.99>quote['Open']:
		
			buyPrice = quote['Open']
			sellPrice = trailingQuote['Close']
			delta = buyPrice-sellPrice
			r = delta/buyPrice
				
	return r
'''

'''
# this is short and up 100%
def calculateReturnForDate(symbol, currentDate, quoteSql):
	quote = quoteSql.fetchForSymbolAndDate(symbol, currentDate)

	r = 0
	
	if not quote:
		pass
	else:
		# sell one share at open price
		sellPrice = quote['Open']
		
		# buy that share back at close price
		buyPrice = quote['Close']
		
		# say sell price is 8 and buy price is 5, then 8 - 5 = 3
		delta = sellPrice-buyPrice
		
		# and return is delta divided by the initial investment (the sell Price)
		r = delta/sellPrice
				
	return r
'''
	
simulate()