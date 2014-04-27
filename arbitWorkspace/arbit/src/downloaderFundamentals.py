import google.downloader
import sched
import datetime
import time
import constants

class downloader:
	schedule = sched.scheduler(time.time, time.sleep)
	
	def __init__(self):
		#don't want to run immediately because we won't get a close price
		today = datetime.date.today()
		downloadTime=constants.downloadtimeFundamentals
		downloadDateTime = datetime.datetime.combine(today, downloadTime)
		downloadTime = time.mktime(downloadDateTime.timetuple())
		
		self.schedule.enterabs(downloadTime, 0, self.download, ())
		self.schedule.run()

	def download(self):
		print ('Running quote download at ' + datetime.datetime.today().isoformat())
	
		# Assume the system clock uses NY time.
		today = datetime.date.today()
		tomorrow = today + datetime.timedelta(days=1)
	
		downloadTime=constants.downloadtimeFundamentals
		downloadDateTime = datetime.datetime.combine(tomorrow, downloadTime)
		downloadTime = time.mktime(downloadDateTime.timetuple())
	
		print ('Downloading...')
	
		google.downloader.run()
		
		# Reschedule the download to run again tomorrow.
		self.schedule.enterabs(downloadTime, 0, self.download, ())
	
		print ('Done with fundamentals download at ' + datetime.datetime.today().isoformat())
		
downloader()