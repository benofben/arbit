import quotesYahoo
import constants
	
def e(self):
	# this is E(Symbol)
	window=100
	e=1.0
	currentIndex=quotesYahoo.getIndex(self.currentDate, self.quotes[self.symbol])
	if currentIndex and currentIndex-window>0:
		for day in range(currentIndex-window, currentIndex):
			Open=self.quotes[self.symbol]['Open'][day]
			unused_Low=self.quotes[self.symbol]['Low'][day]
			High=self.quotes[self.symbol]['High'][day]
			Close=self.quotes[self.symbol]['Close'][day]
			
			# go long
			if(High>Open*(1.0+constants.take)):
				e*=1.0+constants.take
			else:
				e*=1.0+((Close-Open)/Open)	
	return e
