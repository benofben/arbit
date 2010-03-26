import quotesAmeritrade
import datetime

print ('Downloading...')
		
startDate=datetime.date.today()-datetime.timedelta(days=600)
endDate=datetime.date.today()-datetime.timedelta(days=1)
quotesAmeritrade.downloadAllQuotes(startDate, endDate)
			
print ('Done with download at ' + datetime.datetime.today().isoformat())
