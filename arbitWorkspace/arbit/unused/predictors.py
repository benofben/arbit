import yahoo.quotes as q
import constants

def e(currentDate, symbol, quotes, window):
	# this is E(Symbol)
	e=1.0
	currentIndex=q.getIndex(currentDate, quotes[symbol])
	if currentIndex and currentIndex-window>0:
		for day in range(currentIndex-window, currentIndex):
			Open=quotes[symbol]['Open'][day]
			unused_Low=quotes[symbol]['Low'][day]
			High=quotes[symbol]['High'][day]
			Close=quotes[symbol]['Close'][day]
			
			# go long
			if(High>Open*(1.0+constants.take)):
				e*=1.0+constants.take
			else:
				e*=1.0+((Close-Open)/Open)
	return e

def pWin(currentDate, symbol, quotes, window):
	win=0.0
	total=0.0
	currentIndex=q.getIndex(currentDate, quotes[symbol])
	if currentIndex and currentIndex-window>0:
		for day in range(currentIndex-window, currentIndex):
			Open=quotes[symbol]['Open'][day]
			High=quotes[symbol]['High'][day]
			
			# go long
			if(High>Open*(1.0+constants.take)):
				win=win+1.0
			total = total+1.0
	if total>0:
		return win/total
	return 0

def pWinShort(currentDate, symbol, quotes, window):
	win=0.0
	total=0.0
	currentIndex=q.getIndex(currentDate, quotes[symbol])
	if currentIndex and currentIndex-window>0:
		for day in range(currentIndex-window, currentIndex):
			Open=quotes[symbol]['Open'][day]
			Low=quotes[symbol]['Low'][day]
			
			# go long
			if(Low<Open*(1.0-constants.take)):
				win=win+1.0
			total = total+1.0
	if total>0:
		return win/total
	return 0
