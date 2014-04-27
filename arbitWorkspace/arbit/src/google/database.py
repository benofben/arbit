from pymongo import MongoClient
import datetime

class database():
	def __init__(self):
		self.client = MongoClient()
		
	def __del__(self):
		self.client.disconnect()

	def insert(self, fundamentals):
		f = {
				'Symbol' : fundamentals['Symbol'],
				'DownloadDate' : fundamentals['Date'],
				'Dividend' : fundamentals['Dividend'],
				'EPS' : fundamentals['EPS'],
				'Shares' : fundamentals['Shares'],
				'InstitutionalOwnership' : fundamentals['InstitutionalOwnership'],
				'Open' : fundamentals['Open'],
				'High' : fundamentals['High'],
				'Low' : fundamentals['Low'],
				'Close' : fundamentals['Close'],
			}
		self.client.arbit.fundamentals.insert(f)

	def fetch(self, currentDate, symbol):
		d = currentDate
		dt = datetime.datetime(d.year, d.month, d.day)

		fundamentals = self.client.arbit.ratingsChanges.find({'Symbol' : symbol, 'DownloadDate' : dt})
		return fundamentals