import sched
import datetime
import time
import quotesAmeritrade

class downloader:
	schedule = sched.scheduler(time.time, time.sleep)
	
	def __init__(self):
		self.schedule.enterabs(time.time(), 0, self.download, ())
		self.schedule.run()
	
	def download(self):
		print 'Running download at ' + datetime.datetime.today().isoformat()
		
		# Assume the local time is NY time.
		today = datetime.date.today()
		tomorrow = today + datetime.timedelta(days=1)
		
		# 12:00am tomorrow
		downloadTime=datetime.time(0,0,0)
		downloadDateTime = datetime.datetime.combine(tomorrow, downloadTime)
		downloadTime = time.mktime(downloadDateTime.timetuple())

		# Download all the symbols from yesterday
		quotesAmeritrade.downloadQuotesForYesterday()
		
		# Reschedule the download to run again tomorrow.
		self.schedule.enterabs(downloadTime, 0, self.download, ())
	
downloader()