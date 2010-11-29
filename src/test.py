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
			bestSymbol = naiveBayes.run(previousTradingDay, quotes, symbolInformation)
		
			currentDateIndex = quotesYahoo.getIndex(currentDate, quotes[bestSymbol])
			if currentDateIndex:
				# If we have training data
				Open = quotes[bestSymbol]['Open'][currentDateIndex]
				High = quotes[bestSymbol]['High'][currentDateIndex]
				Close = quotes[bestSymbol]['Close'][currentDateIndex]
		
				state = ''
				if High>Open*(1+constants.take):
					state = 'Win'	
					capital*=1+(leverage*constants.take)
				else:
					state = 'Loss'
					capital*=1+(((Close/Open)-1)*leverage)
		
				print(bestSymbol + '\t' + str(currentDate) + '\t' + state + '\t' + str(int(capital)))
		elif currentDate==endDate:
			# This is the most recent day and we don't have training data
			previousTradingDay = quotesYahoo.getPreviousTradingDay(endDate, quotes)
			bestSymbol = naiveBayes.run(previousTradingDay, quotes, symbolInformation)
			print('I think you should buy ' + bestSymbol + ' for ' + str(endDate))
			
		currentDate = currentDate + datetime.timedelta(days=1)

if __name__ == "__main__":
	run()
