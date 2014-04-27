import briefing.downloader
import briefing.database
import datetime
import sched
import time
import constants

class downloader:
	schedule = sched.scheduler(time.time, time.sleep)
	
	def __init__(self):
		self.schedule.enterabs(time.time(), 0, self.download, ())
		self.schedule.run()

	def download(self):
		print ('Running analyst download at ' + datetime.datetime.today().isoformat())
	
		# Assume the system clock uses NY time.
		today = datetime.date.today()
		tomorrow = today + datetime.timedelta(days=1)
	
		downloadTime=constants.downloadtimeAnalysis
		downloadDateTime = datetime.datetime.combine(tomorrow, downloadTime)
		downloadTime = time.mktime(downloadDateTime.timetuple())
	
		print ('Downloading...')
		ratingsChangesDB = briefing.database.database()

		startDate = datetime.date.today()
		endDate = startDate - datetime.timedelta(days=365)
		currentDate = startDate
		while currentDate>=endDate:
			briefing.downloader.getAnalysisForDate(currentDate, ratingsChangesDB)
			currentDate = currentDate - datetime.timedelta(days=1)
	
		# Reschedule the download to run again tomorrow.
		self.schedule.enterabs(downloadTime, 0, self.download, ())
	
		print ('Done with analyst download at ' + datetime.datetime.today().isoformat())
		
downloader()