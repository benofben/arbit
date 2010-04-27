import quotesYahoo
import symbols

import sched
import datetime
import time

class downloaderYahoo:
	schedule = sched.scheduler(time.time, time.sleep)
	
	def __init__(self):
		self.schedule.enterabs(time.time(), 0, self.download, ())
		self.schedule.run()

	def download(self):
		print ('Running download at ' + datetime.datetime.today().isoformat())
	
		# Assume the local time is NY time.
		today = datetime.date.today()
		tomorrow = today + datetime.timedelta(days=1)
	
		# 3:00am tomorrow
		downloadTime=datetime.time(3,0,0)
		downloadDateTime = datetime.datetime.combine(tomorrow, downloadTime)
		downloadTime = time.mktime(downloadDateTime.timetuple())
	
		print ('Downloading...')
	
		# Download everything from scratch
		symbols.downloadSymbols()
		quotesYahoo.downloadAllQuotes()
	
		# Reschedule the download to run again tomorrow.
		self.schedule.enterabs(downloadTime, 0, self.download, ())
	
		print ('Done with download at ' + datetime.datetime.today().isoformat())

downloaderYahoo()