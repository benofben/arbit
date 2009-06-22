import quotesAmeritrade
q = quotesAmeritrade.getAllQuotes()

# q[symbol][day][TimeStamp, Open, High Low Close][bar]

peaks={}
for symbol in q:
	peaks[symbol]=[]
	for day in range(0,len(q[symbol])):
		p=0
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
			
		peaks[symbol].append(p)

print peaks
