import cPickle
import os

def main():
	import datetime
	startDate=datetime.date(2007,10,1)
	endDate=datetime.date(2007,12,1)

	import data
	symbols=data.getSymbols()
	quotes=data.getAllQuotes()

	c=25000
	wins=0
	total=0
	
	for day in range(0, (endDate-startDate).days):
		currentDate=startDate+datetime.timedelta(days=day)

		best_p_vgood=0
		best_symbol=''

		for symbol in symbols:
			# for this symbol, we need the last date the symbol was traded
			index=data.getIndex(currentDate, quotes[symbol])
			if index:
				date=quotes[symbol]['Date'][index-1]
				filename='data/queue/response/' + str(date) + symbol
				if os.path.exists(filename):
					f = open(filename, 'r')
					response=cPickle.load(f)
					p=response['p']

					if p['Good']>best_p_vgood:
						best_p_vgood=p['Good']
						best_symbol=symbol

		# see how we did for today
		if best_symbol:
			index=data.getIndex(currentDate, quotes[best_symbol])

			Open=quotes[best_symbol]['Open'][index]
			Close=quotes[best_symbol]['Close'][index]
			High=quotes[best_symbol]['High'][index]
		
			if High>Open*1.02:
				c=c*1.02
				wins=wins+1
			else:
				c=c*(Close/Open)
			total=total+1
		
			pwin=float(wins)/total
			print str(currentDate) + '\t' \
			+ str(round(c)) +  '\t' \
			+ best_symbol +  '\t' \
			+ str(round(best_p_vgood,5)) + '\t' \
			+ str(round(pwin,5)) + '\t'
main()
