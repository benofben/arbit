import quotesAmeritrade
import datetime

print ('Downloading...')
#quotesAmeritrade.downloadEverything()			

startDate = datetime.datetime(year=2009, month=12, day=15)
endDate=datetime.date.today() - datetime.timedelta(days=1)
quotesAmeritrade.downloadAllQuotes(startDate, endDate)

print ('Done with download at ' + datetime.datetime.today().isoformat())
