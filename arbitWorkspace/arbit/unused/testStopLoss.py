import ameritrade.quotes
import datetime

def run():
	symbol = 'AAPL'
	bucket = [symbol]
	
	startDate = datetime.date.today()- datetime.timedelta(days=365)
	endDate=datetime.date.today()
	quotes = ameritrade.quotes.getQuotesBucket(startDate, endDate, bucket)
	
	#symbolInformation = nasdaq.symbols.downloader.getSymbolInformation()

	capital = 10000
	leverage = 2
	
	#if we lose stop * 100% we are out
	stop = 0.01
	
	# try to classify currentDate using data from currentDate-1 and before
	for day in range(0, len(quotes[symbol])):		
		# Buy at open using leverage
		buyPrice = quotes[symbol][day]['Open'][120]
		highPrice = quotes[symbol][day]['High'][120]
		stoppedOut = False
		
		# run the day
		for bar in range(120, len(quotes[symbol])):
			if (highPrice < quotes[symbol][day]['High'][bar]):
				highPrice = quotes[symbol][day]['High'][bar]
				
			if(quotes[symbol][day]['Low'][bar] < highPrice * (1.0 - stop)):
				#Then we are out at stop
				stoppedOut = True
		
		sellPrice = 0
		if(stoppedOut):
			sellPrice = buyPrice * (1.0 - stop)
		else:
			sellPrice = quotes[symbol][day]['Low'][len(quotes[symbol])-1]
		
		delta = 1+(((sellPrice/buyPrice)-1)*leverage)
		capital = capital * delta
		
		print(str(buyPrice) + '\t' + str(sellPrice) + '\t' + str(stoppedOut) + '\t' + str(capital))
		
# need to check if main for multiprocessing
if __name__ == "__main__":
	run()
