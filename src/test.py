import quotesAmeritrade
import datetime

startDate = datetime.date.today() - datetime.timedelta(days=500)
endDate = datetime.date.today()	
q = quotesAmeritrade.getAllQuotes(startDate, endDate)
# q[symbol][day][TimeStamp, Open, High Low Close][bar]

def run():
	capital=10000
	leverage=2
	
	for dayIndex in range (0,500):
		[symbol, averagePeaks] = predictorAveragePeaks(dayIndex)
		
		o = q[symbol][dayIndex]['Open'][0]
		
		state = False
		
		for timeIndex in range(0, len(q[symbol][dayIndex]['Open'])):
			h=q[symbol][dayIndex]['High'][timeIndex]
			l=q[symbol][dayIndex]['Low'][timeIndex]
			
			'''
			# Stop Loss
			if l<o*0.98:
				capital*=1-(0.02*leverage)
				state="Stop"
				break
			'''
			
			# Win
			if h>o*1.02:
				capital*=1+(.02*leverage)
				state="Win"
				break
			
		if state != "Win" and state != "Stop":
			c=q[symbol][dayIndex]['Close'][timeIndex]
			capital*=(((c/o)-1)*leverage)+1
			state="Loss"
		
		print(symbol + '\t' + state + '\t' + str(q[symbol][dayIndex]['TimeStamp'][timeIndex]) + '\t' + str(int(capital)) + '\t' + str(averagePeaks))

def predictorAveragePeaks(index):
	peaks={}
	averagePeaks={}
	for symbol in q:
		peaks[symbol]=[]
		for day in range(index-3,index):
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
