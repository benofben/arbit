import cx_Oracle
import sys
import constants

class sql():
	def __init__(self):
		self.connection = cx_Oracle.connect('arbit/arbit@orcl')
		
	def create_table(self):
		cursor = self.connection.cursor()		
		sql = 'CREATE TABLE YahooQuotes(Symbol varchar2(5), QuoteDate date, Open float, High float, Low float, Close float, Volume int, AdjClose float, CONSTRAINT YahooQuotesPK PRIMARY KEY (Symbol, QuoteDate))'
		try:
			response = cursor.execute(sql)
			print(response)
		except cx_Oracle.DatabaseError as exc:
			error, = exc.args
			print(sys.stderr, "Oracle-Error-Code:", error.code)
			print(sys.stderr, "Oracle-Error-Message:", error.message)
		self.connection.commit()		
		cursor.close()
	
	def drop_table(self):
		cursor = self.connection.cursor()
		sql = 'DROP TABLE YahooQuotes'
		try:		
			response = cursor.execute(sql)
			print(response)
		except cx_Oracle.DatabaseError as exc:
			error, = exc.args
			print(sys.stderr, "Oracle-Error-Code:", error.code)
			print(sys.stderr, "Oracle-Error-Message:", error.message)
		self.connection.commit()
		cursor.close()

	def __del__(self):
		self.connection.close()

	def insert(self, quote):	
		cursor = self.connection.cursor()
		
		for i in range(0,len(quote['Date'])):			
			cursor.execute("INSERT INTO YahooQuotes(Symbol,QuoteDate,Open,High,Low,Close,Volume,AdjClose) VALUES (:Symbol,:QuoteDate,:Open,:High,:Low,:Close,:Volume,:AdjClose)",
				{
					'Symbol' : quote['Symbol'],
					'QuoteDate' : quote['Date'][i],
					'Open' : quote['Open'][i],
					'High' : quote['High'][i],
					'Low' : quote['Low'][i],
					'Close' : quote['Close'][i],
					'Volume' : quote['Volume'][i],
					'AdjClose' : quote['AdjClose'][i],
				}
			)
		self.connection.commit()
		cursor.close()
					
	def fetchInformation(self, symbol):
		cursor = self.connection.cursor()
		
		cursor.execute("SELECT Symbol, QuoteDate, Open, High, Low, Close, Volume FROM YahooQuotes WHERE Symbol=:symbol AND QuoteDate BETWEEN :StartDate AND :EndDate",
			Symbol = symbol,
			StartDate = constants.startDate,
			EndDate = constants.endDate
		)
		
		trainingInformation = {}
		trainingInformation['QuoteDate']=[]
		trainingInformation['Open']=[]
		trainingInformation['High']=[]
		trainingInformation['Low']=[]
		trainingInformation['Close']=[]
		trainingInformation['Volume']=[]

		rows = cursor.fetchall()
		if not rows:
			return None
		
		for row in rows:
			# Symbol is Index 0
			trainingInformation['QuoteDate'].append(row[1])			
			trainingInformation['Open'].append(row[2])
			trainingInformation['High'].append(row[3])
			trainingInformation['Low'].append(row[4])
			trainingInformation['Close'].append(row[5])
			trainingInformation['Volume'].append(row[6])
		cursor.close()
		
		return trainingInformation
