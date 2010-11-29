import quotesYahoo
import constants
import naiveBayes
import symbols
import datetime

def run():
	#bucket = ['AAPL', 'AMGN', 'ACOR', 'F']
	#quotes = quotesYahoo.getQuotesBucket(bucket)
	quotes = quotesYahoo.getAllQuotes()
	symbolInformation = symbols.getSymbolInformation()

	capital = 10000
	leverage = 2

	currentDate = datetime.date.today() - datetime.timedelta(days=30)
	endDate = datetime.date.today()
	
	# try to classify currentDate using data from currentDate-1 and before
	while currentDate<=endDate:
		
		if(quotesYahoo.isTradingDay(currentDate, quotes)):
			previousTradingDay = quotesYahoo.getPreviousTradingDay(currentDate, quotes)
			bestSymbols = naiveBayes.run(previousTradingDay, quotes, symbolInformation)
		
			results = ''
			newCapital=0
			for symbol in bestSymbols:
				currentDateIndex = quotesYahoo.getIndex(currentDate, quotes[symbol])
				if not currentDateIndex:
					# then do nothing
					newCapital = newCapital + capital/len(bestSymbols)
				if currentDateIndex:
					# If we have training data
					Open = quotes[symbol]['Open'][currentDateIndex]
					High = quotes[symbol]['High'][currentDateIndex]
					Close = quotes[symbol]['Close'][currentDateIndex]
		
					if High>Open*(1+constants.take):	
						newCapital = newCapital + capital/len(bestSymbols)*(1+(leverage*constants.take))
						results = results + symbol + '=' + 'Win' + '\t'
					else:
						newCapital = newCapital + capital/len(bestSymbols)*(1+(((Close/Open)-1)*leverage))
						results = results + symbol + '=' + 'Loss' + '\t'
			capital = newCapital
			print(str(currentDate) + '\t' + str(int(capital))+ '\t' + results)
		elif currentDate==endDate:
			# This is the most recent day and we don't have training data
			previousTradingDay = quotesYahoo.getPreviousTradingDay(endDate, quotes)
			bestSymbols = naiveBayes.run(previousTradingDay, quotes, symbolInformation)
			print('I think you should buy ' + str(bestSymbols) + ' for ' + str(endDate))
			
		currentDate = currentDate + datetime.timedelta(days=1)

# need to check if main for multiprocessing
if __name__ == "__main__":
	run()
