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
			try:
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
			except cx_Oracle.IntegrityError:
				# Yahoo now occasionally duplicates the second to last quote.  For example, if it's 7/3/12, there will be two copies of 7/2/12.  Ignoring the second entry.
				pass
			
		self.connection.commit()
		cursor.close()
					
	def fetchForSymbol(self, symbol):
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

	def fetchForSymbolAndDate(self, symbol, currentDate):
			# make a date that Oracle likes.  This avoids having to do <, >= tricks with a proper Oracle date.
			currentDate = currentDate.strftime('%d-%b-%y')
			
			cursor = self.connection.cursor()
			
			cursor.execute("SELECT Symbol, QuoteDate, Open, High, Low, Close, Volume FROM YahooQuotes WHERE Symbol=:symbol AND QuoteDate=:CurrentDate",
				Symbol = symbol,
				CurrentDate = currentDate
			)
	
			rows = cursor.fetchall()
			if not rows:
				return None
			
			quote = {}
			quote['Symbol']=rows[0][1]
			quote['QuoteDate']=rows[0][1]
			quote['Open']=rows[0][2]
			quote['High']=rows[0][3]
			quote['Low']=rows[0][4]
			quote['Close']=rows[0][5]
			quote['Volume']=rows[0][6]
	
			cursor.close()
			
			return quote
