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
		capital = simulateForDate(currentDate, capital, upgradeSql, quoteSql)
		print(currentDate.isoformat() + '\t$' + str(capital))
		currentDate = currentDate + datetime.timedelta(days=6)

def simulateForDate(currentDate, capital, upgradeSql, quoteSql):
	upgrades = upgradeSql.fetch(currentDate - datetime.timedelta(days=1))
	
	# Check if there are upgrades to trade on today.
	if(not upgrades):
		return capital
	
	capitalPerUpgrade = capital / len(upgrades)
	capital = 0
	
	for upgrade in upgrades:
		r = calculateReturnForDate(upgrade['Ticker'], currentDate, quoteSql)
		capital = capital + capitalPerUpgrade * r
		
	capital = round(capital, 2)
	
	return capital
	
def calculateReturnForDate(symbol, currentDate, quoteSql):
	startQuote = quoteSql.fetchForSymbolAndDate(symbol, currentDate)
	endQuote = quoteSql.fetchForSymbolAndDate(symbol, currentDate + datetime.timedelta(days=6))
	
	if not startQuote or not endQuote:
		r = 1
	else:
		r = startQuote['Open']/endQuote['Open']
	
	return r
	
simulate()