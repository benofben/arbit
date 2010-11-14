import sched
import datetime
import time
import quotesAmeritrade
import os
import csv
import shutil
import constants

class downloaderAmeritrade:
	schedule = sched.scheduler(time.time, time.sleep)
	
	def __init__(self):
		self.schedule.enterabs(time.time(), 0, self.download, ())
		self.schedule.run()
	
	def __prune(self):
		# first, nuke the prune directory
		print ('Cleaning up the prune directory.')
		if os.path.exists(constants.dataDirectory + 'ameritrade/pruned'):
			shutil.rmtree(constants.dataDirectory + 'ameritrade/pruned')
		
		print ('Copying the pruned quotes.')
		symbols = os.listdir(constants.dataDirectory + 'ameritrade/quotes')
		for symbol in symbols:
			# Load the price history from the most recent trading day.
			files = os.listdir(constants.dataDirectory + 'ameritrade/quotes/' + symbol)
			if(len(files)-1>0):
				filename = constants.dataDirectory + 'ameritrade/quotes/' + symbol + '/' + files[len(files)-1]
				
				if not os.path.isdir(filename):
					file = open(filename,'r')
					reader=csv.reader(file)
					
					# Figure out what the total volume was that day.
					v=0
					for TimeStamp, Open, High, Low, Close, Volume in reader:
						v+=float(Volume)
					
					file.close()
					
					# If the total volume for the most recent day  was greater than 1,000,000 then copy the data into pruned.
					# These symbols screened back in symbols to have a market cap > $1 billion
					if v>1000000:
						shutil.copytree(constants.dataDirectory + 'ameritrade/quotes/' + symbol, constants.dataDirectory + 'ameritrade/pruned/' + symbol)
	
	def download(self):
		print ('Running download at ' + datetime.datetime.today().isoformat())
		
		# Assume the local time is NY time.
		today = datetime.date.today()
		tomorrow = today + datetime.timedelta(days=1)
		
		# 12:00am tomorrow
		downloadTime=datetime.time(0,0,0)
		downloadDateTime = datetime.datetime.combine(tomorrow, downloadTime)
		downloadTime = time.mktime(downloadDateTime.timetuple())
		
		print ('Downloading...')
		
		startDate=datetime.date.today()-datetime.timedelta(days=1)
		endDate=datetime.date.today()-datetime.timedelta(days=1)
		quotesAmeritrade.downloadAllQuotes(startDate, endDate)
		
		# This eliminates low volume symbols
		self.__prune()
		
		# Reschedule the download to run again tomorrow.
		self.schedule.enterabs(downloadTime, 0, self.download, ())
		
		print ('Done with download at ' + datetime.datetime.today().isoformat())

downloaderAmeritrade()
