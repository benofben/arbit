import datetime
import time
import sched
import ameritrade
import constants

class arbit:
	best_symbol = None
	sellOrderid = None
	schedule = sched.scheduler(time.time, time.sleep)
	
	def __init__(self):
		self.schedule.enterabs(time.time(), 0, self.pretrade, ())
		self.schedule.run()
	
	def pretrade(self):
		print 'Running pretrade at ' + datetime.datetime.today().isoformat()
		
		# Assume the local time is NY time.
		today = datetime.date.today()
		tomorrow = today + datetime.timedelta(days=1)
		
		# 9:28am today
		openPositionsTime=datetime.time(9,28,0)
		openPositionsDatetime = datetime.datetime.combine(today, openPositionsTime)
		openPositionsTime = time.mktime(openPositionsDatetime.timetuple())
		
		# 3:57pm today
		closePositionsTime=datetime.time(15,57,0)
		closePositionsDatetime = datetime.datetime.combine(today, closePositionsTime)
		closePositionsTime = time.mktime(closePositionsDatetime.timetuple())
		
		# 12:00am tomorrow
		pretradeTime=datetime.time(0,0,0)
		pretradeDateTime = datetime.datetime.combine(tomorrow, pretradeTime)
		pretradeTime = time.mktime(pretradeDateTime.timetuple())
		
		# Is it a weekday?  We're assuming all weekdays are trading days.
		if today.weekday()<5:
			self.download()
			self.best_symbol=self.findBestSymbol()
			print 'The best symbol is ' + self.best_symbol + '.'
			
			# Is it before 9:28am? If not we should skip today
			if time.time()<openPositionsTime:
				print 'Scheduling trades for today.'		
				self.schedule.enterabs(openPositionsTime, 0, self.openPositions, ())
				self.schedule.enterabs(closePositionsTime, 0, self.closePositions, ())
		
		# Reschedule the pretrade to run again tomorrow.
		self.schedule.enterabs(pretradeTime, 0, self.pretrade, ())
	
	def download(self):
		# import symbols
		#symbols.downloadSymbols()
		
		# import quotes
		#quotes.downloadAllQuotes()
		
		# we're only going to grab the IBS bucket for now
		# note that if one of these symbols is delisted, we're going to keep
		# using the most recent update... not good.
		import updateibsbucket
		updateibsbucket.update()
		print 'Download done at ' + datetime.datetime.today().isoformat()
	
	def findBestSymbol(self):	
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
		print 'Classification done at ' + datetime.datetime.today().isoformat()
		return symbol
	
	def openPositions(self):
		print 'Opening positions at ' + datetime.datetime.today().isoformat()
		
		atd = ameritrade.ameritrade()
		logIn = atd.LogIn()	
		if logIn['result'][0]=='OK':
			accountid=logIn['xml-log-in'][0]['associated-account-id'][0]
			
			balancesAndPositions = atd.BalancesAndPositions()
			roundtrips=int(balancesAndPositions['balance'][0]['round-trips'][0])
			accountvalue=float(balancesAndPositions['balance'][0]['account-value'][0]['initial'][0])
			stockbuyingpower=float(balancesAndPositions['balance'][0]['stock-buying-power'][0])
			
			# check if we can day trade
			if accountvalue>25000 or roundtrips<4:
				print 'I am going to trade today.'
				
				# get the bid price (if we're patient, we can probably buy at bid)
				snapshotQuotes=atd.SnapshotQuotes(self.best_symbol)
				bid=float(snapshotQuotes['quote-list'][0]['quote'][0]['bid'][0])
				
				# figure out how many shares we can safely afford
				quantity=int((stockbuyingpower*0.95-10)/bid)
				if quantity==0:
					print 'We do not have enough cash to trade.'
					atd.LogOut()
					return
				
				# place a limit order to buy at the bid price
				orderString='action=buy~quantity=' + str(quantity) + '~symbol=' + self.best_symbol + '~ordtype=Limit~price=' + str(bid) + '~expire=day~accountid=' + accountid
				print orderString
				equityTrade=atd.EquityTrade(orderString)
				
				if equityTrade['order-wrapper'][0]['error'][0]!=None:
					print 'Could not place buy order.'
					print equityTrade
					atd.LogOut()
					return
				
				# now let's wait until our order is processsed
				print 'Waiting for order to fill...'
				buyOrderid=equityTrade['order-wrapper'][0]['order'][0]['order-id'][0]
				status=''
				startTime=time.time()
				while status!='Filled':
					orderStatus=atd.OrderStatus(buyOrderid)
					status=orderStatus['orderstatus-list'][0]['orderstatus'][0]['display-status'][0]
					
					# we've waited 5 minutes, let's just cancel the buy order
					if time.time()>startTime+5*60:
						print 'Waited 5 minutes, going to cancel the buy order.'
						orderCancel=atd.OrderCancel(buyOrderid)
						
						if orderCancel['result'][0]!='OK':
							print 'Could not cancel order.'
							print orderCancel
							atd.LogOut()
							return
						
						break
					
					time.sleep(5)
				
				# The order was filled, partially filled, or was cancelled before filling at all
				# Figure out the average fill price and the quantity filled
				averageFillPrice=0
				totalFillQuantity=0
				try:
					fills=orderStatus['orderstatus-list'][0]['orderstatus'][0]['fills']
					for fill in fills:
						fillQuantity=float(fill['fill-quantity'][0])
						fillPrice=float(fill['fill-price'][0])
						totalFillQuantity+=fillQuantity
						averageFillPrice+=fillQuantity*fillPrice
					averageFillPrice/=totalFillQuantity
					print str(fillQuantity) + 'shares filled at ' + str (averageFillPrice)
				except KeyError:
					print 'Buy order not filled.'
				
				# place sell order
				if totalFillQuantity>0:
					price=averageFillPrice*(1+constants.take)
					orderString='action=sell~quantity=' + str(totalFillQuantity) + '~symbol=' + self.best_symbol + '~ordtype=Limit~price=' + price + '~expire=day~accountid=' + accountid
					print orderString
					equityTrade=atd.EquityTrade(orderString)
						
					if equityTrade['order-wrapper'][0]['error'][0]!=None:
						print 'Could not place sell order.'
						print equityTrade
						atd.LogOut()
						return
					
					self.sellOrderid=equityTrade['order-wrapper'][0]['order'][0]['order-id'][0]
		
		atd.LogOut()
	
	def closePositions(self):
		print 'Closing positions at ' + datetime.datetime.today().isoformat()
		
		if not self.sellOrderid:
			print 'No sell order.  Nothing to do.'
			return
		
		atd = ameritrade.ameritrade()
		logIn = atd.LogIn()	
		if logIn['result'][0]=='OK':
			accountid=logIn['xml-log-in'][0]['associated-account-id'][0]
			
			# Is the sell order still open?
			orderStatus=atd.OrderStatus(self.sellOrderid)
			status=orderStatus['orderstatus-list'][0]['orderstatus'][0]['display-status'][0]
			
			if status == 'Filled':
				print 'We won today!  All closed out.'
			else:
				print 'We lost today.'
				
				# Get the current price
				snapshotQuotes=atd.SnapshotQuotes(self.best_symbol)
				bid=float(snapshotQuotes['quote-list'][0]['quote'][0]['bid'][0])
				
				# Modify the order to market price limit with goot till closed extended hours (gtc_ext)
				remainingQuantity=orderStatus['orderstatus-list'][0]['orderstatus'][0]['remaining-quantity'][0]
				orderString='orderid=' + self.sellOrderid + '~accountid=' + accountid + '~expire=day_ext~ordtype=limit~price=' + str(bid) + '~quantity=' + remainingQuantity
				editOrder=atd.EditOrder(orderString)
				
				if editOrder['order-wrapper'][0]['error'][0]!=None:
					print 'Could not edit order.'
					print editOrder
					atd.LogOut()
					return
		
		atd.LogOut()

arbit()