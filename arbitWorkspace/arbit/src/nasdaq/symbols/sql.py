import cx_Oracle
import sys

class sql():
	def __init__(self):
		self.connection = cx_Oracle.connect('arbit/arbit@orcl')		
		
	def create_table(self):	
		cursor = self.connection.cursor()
		sql = 'CREATE TABLE NASDAQSymbolInformation(Symbol varchar2(9), Exchange varchar2(6), updateDate date, Name varchar(99), LastSale number(8,2), MarketCap number(14,2), IPOYear number(4), Sector varchar(21), Industry varchar(62), CONSTRAINT NASDAQSymbolInformationPK PRIMARY KEY (Symbol, Exchange, updateDate))'
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
		sql = 'DROP TABLE NASDAQSymbolInformation'
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

	def insert(self, symbolInformation):	
		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO NASDAQSymbolInformation(Symbol,Exchange,updateDate,Name,LastSale,MarketCap,IPOYear,Sector,Industry) VALUES (:Symbol,:Exchange,:updateDate,:Name,:LastSale,:MarketCap,:IPOYear,:Sector,:Industry)",
			{
				'Symbol' : symbolInformation['Symbol'],
				'Exchange' : symbolInformation['Exchange'],
				'updateDate' : symbolInformation['Date'],
				'Name' : symbolInformation['Name'],
				'LastSale' : symbolInformation['LastSale'],
				'MarketCap' : symbolInformation['MarketCap'],
				'IPOYear' : symbolInformation['IPOYear'],
				'Sector' : symbolInformation['Sector'],
				'Industry' : symbolInformation['Industry'],
			}
		)
		self.connection.commit()
		cursor.close()
	
	def fetchSymbols(self):
		cursor = self.connection.cursor()
		
		cursor.execute("select Symbol from NASDAQSymbolInformation")
		symbols = []
		for row in cursor.fetchall():
			symbols.append(row[0])
		cursor.close()
		
		return symbols
		
	def fetchInformation(self, symbol):
		cursor = self.connection.cursor()
		
		cursor.execute("SELECT Symbol, Exchange, IPOYear, Sector, Industry, MarketCap FROM NASDAQSymbolInformation WHERE Symbol=:symbol",
			Symbol=symbol
		)
			
		row = cursor.fetchall()[0]
		trainingInformation = {}
		trainingInformation['Symbol'] = row[0]
		trainingInformation['Exchange'] = row[1]
		trainingInformation['IPOYear'] = row[2]
		trainingInformation['Sector'] = row[3]
		trainingInformation['Industry'] = row[4]
		trainingInformation['MarketCap'] = row[5]
		cursor.close()
		
		return trainingInformation

