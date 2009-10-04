import quotesAmeritrade
import datetime

startDate = datetime.date.today() - datetime.timedelta(days=90)
endDate = datetime.date.today()	
q = quotesAmeritrade.getAllQuotes(startDate, endDate)
# q[symbol][day][TimeStamp, Open, High Low Close][bar]

def run():
	capital=10000
	
	for i in range (0,50):
		[symbol, averagePeaks] = predictorAveragePeaks(i)

		Open = q[symbol][i]['Open'][0]
		
		High = 0
		for h in q[symbol][i]['High']:
			if h>High:
				High=h
		
		Close = q[symbol][i]['Close'][len(q[symbol][i]['Close'])-1]
		
		leverage=2.5
		if High>Open*1.02:
			capital*=1+(.02*leverage)
		else:
			capital*=1 - ((1 - Close/Open)*leverage)
			
		print (symbol + '\t' + str(q[symbol][i]['TimeStamp'][0]) + '\t' + str(int(capital)) + '\t' + str(averagePeaks))
		

def predictorAveragePeaks(index):
	peaks={}
	averagePeaks={}
	for symbol in q:
		peaks[symbol]=[]
		for day in range(index-5,index):
			p=0
			try:
				t0=q[symbol][day]['Open'][0]
		
				t=0
				target='high'
				while t<len(q[symbol][day]['High']):
					if target=='high' and q[symbol][day]['High'][t]>t0*1.02:
						p=p+1
						target='low'

					if target=='low' and q[symbol][day]['Low'][t]<=t0:
						target='high'	
					t=t+1
			except IndexError:
				pass
			peaks[symbol].append(p)
		
		averagePeaks[symbol]=0.0
		for p in peaks[symbol]:
			averagePeaks[symbol]+=p
		averagePeaks[symbol]/=len(peaks[symbol])

	b = dict(map(lambda item: (item[1],item[0]),averagePeaks.items()))
	symbol = b[max(b.keys())]
	return [symbol,averagePeaks[symbol]]

run()













