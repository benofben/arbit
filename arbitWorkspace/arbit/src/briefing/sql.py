import cx_Oracle
import sys

class sql():
	def __init__(self):
		self.connection = cx_Oracle.connect('arbit/arbit@orcl')		
		
	def create_table(self):	
		cursor = self.connection.cursor()
		sql = 'CREATE TABLE RatingsChanges(RatingsChangeDate date, RatingsChangeType varchar(10), Company varchar(39), Ticker varchar(8), BrokerageFirm varchar(26), RatingsChange varchar(35), PriceTarget varchar(35), CONSTRAINT AnalystUpgradesPK PRIMARY KEY (RatingsChangeDate, RatingsChangeType, Ticker, BrokerageFirm))'
		
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
		sql = 'DROP TABLE RatingsChanges'
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

	def insert(self, change):
		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO RatingsChanges(RatingsChangeDate, RatingsChangeType, Company, Ticker, BrokerageFirm, RatingsChange, PriceTarget) VALUES (:RatingsChangeDate, :RatingsChangeType, :Company, :Ticker, :BrokerageFirm, :RatingsChange, :PriceTarget)",
			{
				'RatingsChangeDate' : change['RatingsChangeDate'],
				'RatingsChangeType' : change['RatingsChangeType'],
				'Company' : change['Company'],
				'Ticker' : change['Ticker'],
				'BrokerageFirm' : change['BrokerageFirm'],
				'RatingsChange' : change['RatingsChange'],
				'PriceTarget' : change['PriceTarget'],
			}
		)
		self.connection.commit()
		cursor.close()
		
	def fetch(self, currentDate, ratingsChangeType):
		cursor = self.connection.cursor()
		
		cursor.execute("SELECT RatingsChangeDate, RatingsChangeType, Company, Ticker, BrokerageFirm, RatingsChange, PriceTarget FROM RatingsChanges WHERE RatingsChangeDate=:CurrentDate AND RatingsChangeType=:RatingsChangeType",
			RatingsChangeType = ratingsChangeType,
			CurrentDate = currentDate
		)
		
		rows = cursor.fetchall()
		if not rows:
			return None
		
		changes = []		
		for row in rows:
			change = {}
			change['RatingsChangeDate']=row[0]
			change['RatingsChangeType']=row[1]
			change['Company']=row[2]
			change['Ticker']=row[3]
			change['BrokerageFirm']=row[4]
			change['RatingsChange']=row[5]
			change['PriceTarget']=row[6]
			changes.append(change)
		cursor.close()
		
		return changes
