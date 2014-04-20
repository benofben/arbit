import datetime
import briefing.sql
import yahoo.sql

def run():
	capital = 0

	upgradeSql = briefing.sql.sql()
	quoteSql = yahoo.sql.sql()
	
	startDate = datetime.date.today() - datetime.timedelta(days=365)
	endDate = datetime.date.today()# - datetime.timedelta(days=200)
	currentDate = startDate

	while currentDate<endDate:
		[capital, symbols] = runForDate(currentDate, capital, upgradeSql, quoteSql)
		print(currentDate.isoformat() + '\t' + str(currentDate.isoweekday()) +'\t$' + str(capital) + '\t' + str(symbols))
		currentDate = currentDate + datetime.timedelta(days=1)

def runForDate(currentDate, capital, upgradeSql, quoteSql):
	upgrades = upgradeSql.fetch(currentDate - datetime.timedelta(days=1), 'Upgrade')
	symbols=[]
	
	# Check if there are upgrades to trade on today.
	if(not upgrades):
		return [capital, symbols]
	
	for upgrade in upgrades:
		r = calculateReturnForDate1(upgrade['Ticker'], currentDate, quoteSql)
		if r!=0:
			symbols.append([upgrade['Ticker'], r])
	
	if len(symbols)>0:
		for [unused_ticker, r] in symbols:
			capital = capital + (10000 * r)
		capital = round(capital, 2)
	
	return [capital, symbols]

def calculateReturnForDate_SimpleLong(symbol, currentDate, quoteSql):
	
	'''
	Long
	buy at $10
	sell at $12
	return is (10-12)/10
	return is sell-buy/buy
	'''
	
	quote = quoteSql.fetchForSymbolAndDate(symbol, currentDate)

	r = 0
	
	if not quote:
		pass
	else:
		buyPrice = quote['Open']
		sellPrice = quote['Close']
		r = (sellPrice - buyPrice) / buyPrice

	return r
	
def calculateReturnForDate_SimpleShort(symbol, currentDate, quoteSql):

	'''
	Short
	sell at $10
	buy at $8
	return is (10-8)/10
	return is sell-buy/sell
	'''

	quote = quoteSql.fetchForSymbolAndDate(symbol, currentDate)

	r = 0
	
	if not quote:
		pass
	else:
		sellPrice = quote['Open']
		buyPrice = quote['Close']
		r = (sellPrice - buyPrice) / sellPrice

	return r

def calculateReturnForDate1(symbol, currentDate, quoteSql):
	
	#what if we just buy and put in trailing stops?

	quote = quoteSql.fetchForSymbolAndDate(symbol, currentDate)
	futureQuote = quoteSql.fetchForSymbolAndDate(symbol, currentDate + datetime.timedelta(days=3))

	r = 0
	
	if not quote or not futureQuote:
		pass
	else:		
		buyPrice = quote['Open']
		sellPrice = futureQuote['Close']
		r = (sellPrice - buyPrice) / buyPrice

	return r

# this is doing reasonably well. +3k over 4 months.
def calculateReturnForDate2(symbol, currentDate, quoteSql):
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

# this is short and up 100%
def calculateReturnForDate3(symbol, currentDate, quoteSql):
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

run()