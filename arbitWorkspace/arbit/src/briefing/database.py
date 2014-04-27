from pymongo import MongoClient
import datetime

class database():
	def __init__(self):
		self.client = MongoClient()
	
	def __del__(self):
		self.client.disconnect()

	def insert(self, change):
		# BSON (which mongodb uses) only supports datetime, so we need to convert the date.  
		# The hour and minute will be 0
		d = change['RatingsChangeDate']
		dt = datetime.datetime(d.year, d.month, d.day)

		symbol = {
				'RatingsChangeDate' : dt,
				'RatingsChangeType' : change['RatingsChangeType'],
				'Company' : change['Company'],
				'Ticker' : change['Ticker'],
				'BrokerageFirm' : change['BrokerageFirm'],
				'RatingsChange' : change['RatingsChange'],
				'PriceTarget' : change['PriceTarget'],
			}
		self.client.arbit.ratingsChanges.insert(symbol)
		
	def fetch(self, currentDate, ratingsChangeType):
		d = currentDate
		dt = datetime.datetime(d.year, d.month, d.day)

		ratingsChanges=[]
		for change in self.client.arbit.ratingsChanges.find({'RatingsChangeDate' : dt, 'RatingsChangeType' : 'Upgrade'}):
			ratingsChanges.append(change)
		return ratingsChanges