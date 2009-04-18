class tradingday(object):
	import time, sched
	schedule = sched.scheduler(time.time, time.sleep)

	# going to assume the local time is NY time
	# going to assume the market is open every weekday 

	def Pretrade():
		print ('Pretrade')

	def OpenPositions():
		print ('Open Positions')
	
	def ClosePositions():
		print ('Close Positions')
		
		# when we start up, we want to schedule for the next events.  Then everytime
# one of them runs, we want it to reschedule itself for the next trading day

# what if the buy fails?

# download and process at 6:00pm

# need to figure out if 6pm today has passed
# if it has not, then schedule for 6pm today
# else 6pm tomorrow

schedule.enterabs(time.time()+5, 1, Pretrade, ())

# need to enter a trade a 9:25am for market price
schedule.enterabs(time.time()+10, 1, OpenPositions, ())

# close out positions at 3:55pm
schedule.enterabs(time.time()+15, 1, ClosePositions, ())

schedule.run()