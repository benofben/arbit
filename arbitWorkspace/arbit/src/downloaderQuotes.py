import datetime
import nasdaq.symbols.downloader
#import yahoo.quotes

def download():
	print ('Starting quote download at ' + datetime.datetime.today().isoformat())
	nasdaq.symbols.downloader.run()
	#yahoo.quotes.downloadAllQuotes()
	print ('Done with quote download at ' + datetime.datetime.today().isoformat())

download()