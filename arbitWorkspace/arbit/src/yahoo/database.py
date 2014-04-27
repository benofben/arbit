from pymongo import MongoClient
import datetime

class database():
	def __init__(self):
		self.client = MongoClient()
	
	def dropCollection(self):
		self.client.arbit.yahooQuotes.drop()
	
	def __del__(self):
		self.client.disconnect()

	def insert(self, quotes):
		for i in range(0,len(quotes['Date'])):
			
			# BSON (which mongodb uses) only supports datetime, so we need to convert the date.  
			# The hour and minute will be 0
			d = quotes['Date'][i]
			dt = datetime.datetime(d.year, d.month, d.day)
			
			quote = {
				'Symbol' : quotes['Symbol'],
				'QuoteDate' : dt,
				'Open' : quotes['Open'][i],
				'High' : quotes['High'][i],
				'Low' : quotes['Low'][i],
				'Close' : quotes['Close'][i],
				'Volume' : quotes['Volume'][i],
				'AdjClose' : quotes['AdjClose'][i],
			}
			self.client.arbit.yahooQuotes.insert(quote)

			# Yahoo now occasionally duplicates the second to last quote.  
			# For example, if today is 7/3/12, there will be two copies of 7/2/12.
			# I think mongodb is just overwriting the first value with the second.
