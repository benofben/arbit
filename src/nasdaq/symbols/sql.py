import cx_Oracle
import sys

class sql():
	def __init__(self):
		self.connection = cx_Oracle.connect('arbit/arbit@orcl')
		
		self.drop_table()
		
		cursor = self.connection.cursor()
		try:
			sql = 'CREATE TABLE NASDAQSymbolInformation(Symbol varchar2(8), Exchange varchar2(6), updateDate date, Name varchar(99), LastSale number(8,2), MarketCap number(14,2), IPOYear number(4), Sector varchar(21), Industry varchar(62))'
			response = cursor.execute(sql)
			print(response)
		except cx_Oracle.DatabaseError as exc:
			error, = exc.args
			print(sys.stderr, "Oracle-Error-Code:", error.code)
			print(sys.stderr, "Oracle-Error-Message:", error.message)
		self.connection.commit()
		cursor.close()
	
	def drop_table(self):
		sql = 'DROP TABLE NASDAQSymbolInformation'
		cursor = self.connection.cursor()
		response = cursor.execute(sql)
		print(response)
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
	
	def fetch(self):
		cursor = self.connection.cursor()
		cursor.execute("SELECT COUNT(*) FROM NASDAQSymbolInformation")
		count = cursor.fetchall()[0][0]
		print ('count in fetch is ' + str(count))
		
		cursor.execute("select Symbol, Exchange, Name from NASDAQSymbolInformation")

		for column_1, column_2, column_3 in cursor.fetchall():
			print('Values from DB: ', column_1, column_2, column_3)

		cursor.close()
		
