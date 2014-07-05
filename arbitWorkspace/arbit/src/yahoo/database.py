from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import datetime

class database():
	def __init__(self):
		self.client = MongoClient()
		self.client.arbit.yahooQuotes.create_index([("Symbol", DESCENDING), ("Date", ASCENDING)])

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
				'Date' : dt,
				'Open' : quotes['Open'][i],
				'High' : quotes['High'][i],
				'Low' : quotes['Low'][i],
				'Close' : quotes['Close'][i],
				'Volume' : quotes['Volume'][i],
				'AdjustedClose' : quotes['AdjClose'][i],
			}
			self.client.arbit.yahooQuotes.insert(quote)

			# Yahoo now occasionally duplicates the second to last quote.  
			# For example, if today is 7/3/12, there will be two copies of 7/2/12.
			# I think mongdb is just overwriting the first value with the second.

	def findQuoteForDate(self, date, symbol):
		dt = datetime.datetime(date.year, date.month, date.day)
		quotes = self.client.arbit.yahooQuotes.find({'Symbol' : symbol, 'Date' : dt})
		
		# we're just going to return the first quote in the cursor.  
		# There shouldn't be any duplicates
		# Is there an equivalent to findOne in the pymongo API?  That's what I really want here...
		for quote in quotes:
			return(quote)
		
	def findSubquoteForSymbolWithWindow(self, symbol, currentDate, window):
		# returns a quote for a given symbol over a window currentDate-window<=x<currentDate.
		# A quote from currentDate can then be used for testing
		
		endDatetime = datetime.datetime(currentDate.year, currentDate.month, currentDate.day)
		startDatetime = endDatetime - datetime.timedelta(days=30)
		quotes=[]
		for quote in self.client.arbit.yahooQuotes.find({'Symbol': symbol, 'Date': {'$gte': startDatetime, '$lt': endDatetime}}):
			quotes.append(quote)
		return quotes
