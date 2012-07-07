import yahoo.sql
import constants
import yahoo.quotes
import datetime

print('Loading quotes from database...')
yahooSql = yahoo.sql.sql()
quotes = yahooSql.fetchInformation(constants.testStartDate, constants.testEndDate)
symbols = yahoo.quotes.getUniqueList(quotes['Symbol'])
quotes = yahoo.quotes.reformatQuotes(quotes, symbols)
print('Done loading.')

capital = 25000
date=''

file = open(constants.dataDirectory + 'rapidMinerOutput.csv', 'r')

for line in file:
	columns = line.split(',')
	prediction = columns[-1].replace('\n','').replace('"','')
	symbol = columns[-5].replace('"','')
	try:
		[y,m,d] = columns[-6].replace('"','').split('-')
		date = datetime.date(year=int(y), month=int(m), day=int(d))	

		if prediction == 'W':
			i = yahoo.quotes.getIndex(date, quotes[symbol])
			if i:
				if quotes[symbol]['High'][i]>=quotes[symbol]['Open'][i]*1.02:
					capital *= 1.02
				else:
					capital *= quotes[symbol]['Close'][i]/quotes[symbol]['Open'][i]
			print(symbol + '\t' + str(date) +  '\t' + str(capital))
							
	except ValueError:
		pass

file.close()

