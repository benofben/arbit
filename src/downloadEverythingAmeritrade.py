import quotesAmeritrade
import datetime

print ('Downloading...')	
quotesAmeritrade.downloadEverything()
print ('Done with download at ' + datetime.datetime.today().isoformat())
