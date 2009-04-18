import datetime
import time
import sched

def pretrade():
	print 'pretrade ' + datetime.datetime.today().isoformat()

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
	if today.weekday<5:
		
		# download
		# findBestSymbol
		
		# Is it before 9:28am? If not we should skip today
		if time.time()<openPositionsTime:
			print 'Scheduling trades for today.'		
			schedule.enterabs(openPositionsTime, 0, openPositions, ())
			schedule.enterabs(closePositionsTime, 0, closePositions, ())
	
	# Reschedule the pretrade to run again tomorrow.
	schedule.enterabs(pretradeTime, 0, pretrade, ())
	
def openPositions():
	print 'openPositions ' + datetime.datetime.today().isoformat()
	
def closePositions():
	print 'closePositions ' + datetime.datetime.today().isoformat()

# Assume the local time is NY time.
schedule = sched.scheduler(time.time, time.sleep)
schedule.enterabs(time.time(), 0, pretrade, ())
schedule.run()