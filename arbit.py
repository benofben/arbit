class arbit:
	best_symbol = ''
	quantity=0
	
	def __init__(self):
		# going to assume the local time is NY time
		import time, sched
		schedule = sched.scheduler(time.time, time.sleep)

		# download and process at 12:00am
		self.nightlyBatch()

		# need to enter a trade a 9:28am for market price
		# self.openPositions()
		
		# close out positions at 3:57pm
		# self.closePositions()

		#schedule.enterabs()
		#schedule.run()
	
	def nightlyBatch(self):
		self.download()
		self.best_symbol=self.findBestSymbol()
		print 'The best symbol is: ' + self.best_symbol + '.'

	def download(self):
		import symbols
		#symbols.downloadSymbols()
		
		import quotes
		#quotes.downloadAllQuotes()

	def findBestSymbol(self):
		# there are problems with this approach if symbols are delisted.
		# need to change download to clear out the old information
		
		import data
		symbols=data.getSymbols()
		quotes=data.getAllQuotes()

		import classifier
		p={}
		for symbol in symbols:
			date=quotes[symbol]['Date'][-1]
			my_classifier=classifier.classifier(symbol, date, quotes)	
			r=my_classifier.run()
			p[symbol]=r['Good']

		b = dict(map(lambda item: (item[1],item[0]),p.items()))
		symbol = b[max(b.keys())]		
		return symbol

	def openPositions(self):
		import sys, time
		
		import ameritrade
		atd = ameritrade.ameritrade()

		logIn = atd.LogIn()	
		if logIn['result'][0]=='OK':

			balancesAndPositions = atd.BalancesAndPositions()
			roundtrips=int(balancesAndPositions['balance'][0]['round-trips'][0])
			accountvalue=float(balancesAndPositions['balance'][0]['account-value'][0]['initial'][0])
			stockbuyingpower=float(balancesAndPositions['balance'][0]['stock-buying-power'][0])
			accountid=balancesAndPositions['positions'][0]['account-id'][0]
			
			# check if we can day trade
			if accountvalue>25000 or roundtrips<4:
				print 'I am going to enter a trade.'
			
				# figure out how many shares we can safely afford
				snapshotQuotes=atd.SnapshotQuotes(self.best_symbol)
				bid=float(snapshotQuotes['quote-list'][0]['quote'][0]['bid'][0])
				self.quantity=int((stockbuyingpower*0.95-10)/bid)
				if self.quantity==0:
					print 'We do not have enough cash to trade.'
					sys.exit()

				# place order at market (maybe this should be a limit...)
				# orderstring='action=buy~quantity=400~symbol=DELL~ordtype=Limit~price=6.00~expire=day~accountid=' + accountid
				orderstring='action=buy~quantity=' + str(self.quantity) + '~symbol=' + self.best_symbol + '~ordtype=Market~expire=day~accountid=' + accountid
				equityTrade=atd.EquityTrade(orderstring)
				
				if equityTrade['order-wrapper'][0]['error'][0]!=None:
					print 'Could not place order.'
					print equityTrade
					sys.exit()
				
				# now let's wait until our order is processsed
				orderid=equityTrade['order-wrapper'][0]['order'][0]['order-id'][0]
				status=''
				while status!='Filled':
					orderStatus=atd.OrderStatus(orderid)
					status=orderStatus['orderstatus-list'][0]['orderstatus'][0]['display-status'][0]
					print 'Waiting for order to fill...'
					time.sleep(5)
				
				# place sell order
				
				###########need to write something to figure out the fill price and go from there...
				price=100
				
				orderstring='action=sell~quantity=' + str(quantity) + '~symbol=' + self.best_symbol + '~ordtype=Limit~price=' + price + '~expire=day~accountid=' + accountid
				equityTrade=atd.EquityTrade(orderstring)
				
				if equityTrade['order-wrapper'][0]['error'][0]!=None:
					print 'Could not place order.'
					print equityTrade
					sys.exit()
		
		atd.LogOut()
		
	def closePositions(self):
		import ameritrade
		atd = ameritrade.ameritrade()

		logIn = atd.LogIn()	
		if logIn['result'][0]=='OK':
			orderstring='action=sell~quantity=' + str(quantity) + '~symbol=' + self.best_symbol + '~ordtype=Market~expire=day~accountid=' + accountid
			equityTrade=atd.EquityTrade(orderstring)
				
			if equityTrade['order-wrapper'][0]['error'][0]!=None:
				print 'Could not place order.'
				print equityTrade
				sys.exit()
		atd.LogOut()
		
arbit()