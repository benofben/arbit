import datetime
import yahoo.sql
import edgar.sql

def run():
	profit = 0
	
	quoteSql = yahoo.sql.sql()	
	edgarSql = edgar.sql.sql()
	
	startDate = datetime.date.today() - datetime.timedelta(days=365)
	endDate = datetime.date.today()
	currentDate = startDate

	while currentDate<endDate:
		
		[profitToday, symbols] = runForDate(currentDate, edgarSql, quoteSql)
		capital = len(symbols) * 10000  # this is actually much worse since we're holding for 90 days.
		profit+=profitToday
		
		print(currentDate.isoformat() + '\t' + str(currentDate.isoweekday()) +'\t$' + str(profit)  + '\t' + str(capital))
			
		currentDate = currentDate + datetime.timedelta(days=1)
	
def runForDate(currentDate, edgarSql, quoteSql):
	transactions = edgarSql.fetchForDate(currentDate - datetime.timedelta(days=1))
	symbols=[]
	profit = 0
	
	# Check if there are transactions to trade on today.
	if(not transactions):
		return [0, symbols]
	
	for transaction in transactions:
		r = calculateReturnForDate(transaction, currentDate, quoteSql)
		if r!=0:
			symbols.append([transaction['IssuerTradingSymbol'], r])
	
	if len(symbols)>0:
		for [unused_ticker, r] in symbols:
			profit = profit + (10000 * r)
	
	return [profit, symbols]

def calculateReturnForDate(transaction, currentDate, quoteSql):
	quote = quoteSql.fetchForSymbolAndDate(transaction['IssuerTradingSymbol'], currentDate)
	
	r = 0
	
	value = transaction['TransactionPricePerShare']*transaction['TransactionShares']
	buyPrice = transaction['TransactionPricePerShare']
	sellPrice = buyPrice *1.05
	
	if not quote:
		return r
	elif value<100000:
		return r
	elif quote['Low']<buyPrice:

		# then we own some stock
		for timedelta in range(1,90):
			sellDate = currentDate + datetime.timedelta(days=timedelta)
			quote = quoteSql.fetchForSymbolAndDate(transaction['IssuerTradingSymbol'], sellDate)
			if quote and quote['High']>sellPrice:
				return r
	
	quote = None
	sellDate = currentDate + datetime.timedelta(days=90)
	while not quote:
		quote = quoteSql.fetchForSymbolAndDate(transaction['IssuerTradingSymbol'], sellDate)
		sellDate = sellDate + datetime.timedelta(days=1)
	
	sellPrice = quote['Close']
	r = (sellPrice - buyPrice) / buyPrice			
	return r

run()