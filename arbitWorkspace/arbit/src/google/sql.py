import cx_Oracle
import sys

class sql():
	def __init__(self):
		self.connection = cx_Oracle.connect('arbit/arbit@orcl')
		
	def create_table(self):
		cursor = self.connection.cursor()		
		sql = 'CREATE TABLE Fundamentals(Symbol varchar2(5), DownloadDate date, Dividend float, EPS float, Shares float, InstitutionalOwnership float, CONSTRAINT FundamentalsPK PRIMARY KEY (Symbol, DownloadDate))'
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
		sql = 'DROP TABLE Fundamentals'
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

	def insert(self, fundamentals):	
		cursor = self.connection.cursor()
		
		cursor.execute("INSERT INTO Fundamentals(Symbol,DownloadDate,Dividend,EPS,Shares,InstitutionalOwnership) VALUES (:Symbol,:DownloadDate,:Dividend,:EPS,:Shares,:InstitutionalOwnership)",
			{
				'Symbol' : fundamentals['Symbol'],
				'DownloadDate' : fundamentals['Date'],
				'Dividend' : fundamentals['Dividend'],
				'EPS' : fundamentals['EPS'],
				'Shares' : fundamentals['Shares'],
				'InstitutionalOwnership' : fundamentals['InstitutionalOwnership'],
			}
		)
		
		self.connection.commit()
		cursor.close()
	