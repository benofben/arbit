from pymongo import MongoClient
import datetime

class database():
	def __init__(self):
		self.client = MongoClient()
		
	def __del__(self):
		self.client.disconnect()

	def insert(self, form4Information):
		year = int(form4Information['acceptanceDatetime'][0:4])
		month = int(form4Information['acceptanceDatetime'][4:6])
		day = int(form4Information['acceptanceDatetime'][6:8])
		hour = int(form4Information['acceptanceDatetime'][8:10])
		minute = int(form4Information['acceptanceDatetime'][10:12])
		second = int(form4Information['acceptanceDatetime'][12:14])
		acceptanceDatetime = datetime.datetime(year, month, day, hour, minute, second)
		
		year = int(form4Information['transactionDate'][0:4])
		month = int(form4Information['transactionDate'][5:7])
		day = int(form4Information['transactionDate'][8:10])
		transactionDate = datetime.datetime(year, month, day)

		form4 = {
				'SecDocument' : form4Information['secDocument'],
				'AcceptanceDatetime' : acceptanceDatetime, 
				'IssuerTradingSymbol' : form4Information['issuerTradingSymbol'], 
				'RptOwnerCik' : form4Information['rptOwnerCik'],
				'RptOwnerName' : form4Information['rptOwnerName'], 
				'IsDirector' : form4Information['isDirector'],
				'IsOfficer' : form4Information['isOfficer'],
				'IsTenPercentOwner' : form4Information['isTenPercentOwner'], 
				'IsOther' : form4Information['isOther'],
				'TransactionDate' : transactionDate, 
				'TransactionShares' : form4Information['transactionShares'], 
				'TransactionPricePerShare' : form4Information['transactionPricePerShare'], 
				'TransactionAcquiredDisposed' : form4Information['transactionAcquiredDisposedCode'],
				'SharesOwned' : form4Information['sharesOwned'],
			}
		self.client.arbit.form4.insert(form4)

	def fetch(self, currentDate):
		d = currentDate
		dt = datetime.datetime(d.year, d.month, d.day)

		forms=[]
		for form in self.client.arbit.form4.find({'AcceptanceDatetime' : dt}):
			forms.append(form)
		return forms