import yahoo.quotes as q
import constants
import naiveBayes
import symbols
import datetime

def run():
	#bucket = ['AAPL', 'AMGN', 'ACOR', 'F', 'VSH']
	#quotes = quotesYahoo.getQuotesBucket(bucket)
	quotes = q.getAllQuotes()
	symbolInformation = symbols.getSymbolInformation()

	capital = 10000
	leverage = 2

	currentDate = datetime.date.today() - datetime.timedelta(days=365)
	endDate = datetime.date.today()
	
	# try to classify currentDate using data from currentDate-1 and before
	while currentDate<=endDate:
		
		if(q.isTradingDay(currentDate, quotes)):
			previousTradingDay = q.getPreviousTradingDay(currentDate, quotes)
			bestSymbols = naiveBayes.run(previousTradingDay, quotes, symbolInformation)
			results = ''
			newCapital=0
			for symbol in bestSymbols:
				currentDateIndex = q.getIndex(currentDate, quotes[symbol])
				if not currentDateIndex:
					# then do nothing
					newCapital = newCapital + capital/len(bestSymbols)
					results = results + symbol + '=' + 'NA' + '\t'
				if currentDateIndex:
					# If we have training data
					Open = quotes[symbol]['Open'][currentDateIndex]
					Low = quotes[symbol]['Low'][currentDateIndex]
					Close = quotes[symbol]['Close'][currentDateIndex]
		
					if Low<Open*(1-constants.take):	
						newCapital = newCapital + capital/len(bestSymbols)*(1+(leverage*constants.take))
						results = results + symbol + '=' + 'Win' + '\t'
					else:
						#sold at open
						#bought at close
						delta = 1+(((Open/Close)-1)*leverage)
						newCapital = newCapital + capital/len(bestSymbols)*delta
						results = results + symbol + '=' + 'Loss' + '\t'
			capital = newCapital
			print(str(currentDate) + '\t' + str(int(capital))+ '\t' + results)
		elif currentDate==endDate:
			# This is the most recent day and we don't have training data
			previousTradingDay = q.getPreviousTradingDay(endDate, quotes)
			bestSymbols = naiveBayes.run(previousTradingDay, quotes, symbolInformation)
			print('I think you should buy ' + str(bestSymbols) + ' for ' + str(endDate))
			
		currentDate = currentDate + datetime.timedelta(days=1)

# need to check if main for multiprocessing
if __name__ == "__main__":
	run()
