import briefing.sql as sql
import briefing.analysis
import datetime
import sched
import time

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
	
		# 11:50pm tomorrow
		downloadTime=datetime.time(23,50,0)
		downloadDateTime = datetime.datetime.combine(tomorrow, downloadTime)
		downloadTime = time.mktime(downloadDateTime.timetuple())
	
		print ('Downloading...')

		mySql = sql.sql()
		#mySql.drop_table()
		#mySql.create_table()

		startDate = datetime.date.today()
		endDate = startDate - datetime.timedelta(days=365)
		currentDate = startDate
		while currentDate>=endDate:
			briefing.analysis.getAnalysisForDate(currentDate, mySql)
			currentDate = currentDate - datetime.timedelta(days=1)
	
		# Reschedule the download to run again tomorrow.
		self.schedule.enterabs(downloadTime, 0, self.download, ())
	
		print ('Done with analyst download at ' + datetime.datetime.today().isoformat())
		
downloader()