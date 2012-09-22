import edgar.downloader
import edgar.mail
import sched
import datetime
import time
import constants

class downloader:
	schedule = sched.scheduler(time.time, time.sleep)
	
	def __init__(self):
		self.schedule.enterabs(time.time(), 0, self.download, ())
		self.schedule.run()

	def download(self):
		print ('Running quote download at ' + datetime.datetime.today().isoformat())
	
		# Assume the system clock uses NY time.
		today = datetime.date.today()
		tomorrow = today + datetime.timedelta(days=1)
	
		downloadTime=constants.downloadtimeEDGAR
		downloadDateTime = datetime.datetime.combine(tomorrow, downloadTime)
		downloadTime = time.mktime(downloadDateTime.timetuple())
	
		print ('Downloading...')
	
		edgar.downloader.run()
		edgar.mail.run()
		
		# Reschedule the download to run again tomorrow.
		self.schedule.enterabs(downloadTime, 0, self.download, ())
	
		print ('Done with EDGAR download at ' + datetime.datetime.today().isoformat())
		
downloader()