import cx_Oracle

class sql():
	def __init__(self):
		self.connection = cx_Oracle.connect('arbit/arbit@orcl')
		
	def __del__(self):
		self.connection.close()
	
	def fetchSymbols(self, startDate, endDate):
		cursor = self.connection.cursor()
		cursor.execute("SELECT DISTINCT Symbol FROM YahooQuotes WHERE QuoteDate BETWEEN :StartDate AND :EndDate",
			StartDate = startDate,
			EndDate = endDate
		)
		
		rows = cursor.fetchall()
		
		if not rows:
			return None
		
		symbols=[]
		for row in rows:
			symbols.append(row[0])
		
		cursor.close()		
		return symbols
	
	def fetchOpenHigh(self, symbol, startDate, endDate):
		cursor = self.connection.cursor()
		
		cursor.execute("SELECT Open, High FROM YahooQuotes WHERE Symbol=:symbol AND QuoteDate BETWEEN :StartDate AND :EndDate",
			Symbol = symbol,
			StartDate = startDate,
			EndDate = endDate
		)
		
		trainingInformation = {}
		trainingInformation['Open']=[]
		trainingInformation['High']=[]

		rows = cursor.fetchall()
		if not rows:
			return None
		
		for row in rows:
			trainingInformation['Open'].append(row[0])
			trainingInformation['High'].append(row[1])
		cursor.close()
		
		return trainingInformation
