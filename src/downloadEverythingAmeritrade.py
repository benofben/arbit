import quotesAmeritrade
import datetime

print ('Downloading...')	

startDate = datetime.date(year=2007, month=1, day=1)
endDate = datetime.date.today() - datetime.timedelta(days=1)
quotesAmeritrade.downloadAllQuotes(startDate, endDate)

print ('Done with download at ' + datetime.datetime.today().isoformat())
