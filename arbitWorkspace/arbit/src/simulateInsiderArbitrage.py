import datetime
import yahoo.sql
import edgar.sql

def run():
	capital = 10000
	
	quoteSql = yahoo.sql.sql()	
	edgarSql = edgar.sql.sql()
	
	startDate = datetime.date.today() - datetime.timedelta(days=180)
	endDate = datetime.date.today()
	currentDate = startDate
	
	while currentDate<endDate:
		capital = runForDate(currentDate, capital, edgarSql, quoteSql)		
		print(currentDate.isoformat() + '\t' + str(currentDate.isoweekday()) +'\t$' + str(round(capital,2)))
	
		currentDate = currentDate + datetime.timedelta(days=1)
	
def runForDate(currentDate, capital, edgarSql, quoteSql):
	if currentDate.weekday() == 0:
		transactions = edgarSql.fetch(currentDate - datetime.timedelta(days=3))
	elif currentDate.weekday() == 1 or currentDate.weekday() == 2 or currentDate.weekday() == 3 or currentDate.weekday() == 4:
		transactions = edgarSql.fetch(currentDate - datetime.timedelta(days=1))
	elif currentDate.weekday() == 5 or currentDate.weekday() == 6:
		return capital
	
	if not transactions:
		return capital

	symbolsAndReturns=[]	
	for transaction in transactions:
		r = calculateReturnForDate(transaction, currentDate, quoteSql)
		if r!=0:
			symbolsAndReturns.append([transaction['IssuerTradingSymbol'], r])
	
	if len(symbolsAndReturns)>0:
		for [unused_symbol, r] in symbolsAndReturns:
			capital = capital + (1000 * r)
			
	return capital

def calculateReturnForDate(transaction, currentDate, quoteSql):
	quote = quoteSql.fetchForSymbolAndDate(transaction['IssuerTradingSymbol'], currentDate)
	if not quote:
		return 0
	
	value = transaction['TransactionPricePerShare']*transaction['TransactionShares']
	if value<100000:
		return 0

	buyPrice = transaction['TransactionPricePerShare']	
	if buyPrice<quote['Low']:
		return 0
	
	if quote['Low']<=buyPrice:
		# then we own some stock, now let's try to sell it
		quote = None
		sellDate = currentDate + datetime.timedelta(days=90)
		while not quote:
			quote = quoteSql.fetchForSymbolAndDate(transaction['IssuerTradingSymbol'], sellDate)
			sellDate = sellDate + datetime.timedelta(days=1)

		sellPrice = quote['Close']
		capital = 10000
		sharesPurchased = capital/buyPrice
		newCapital = sharesPurchased*sellPrice
		r = newCapital/capital
		r = r-1
		return r

run()