import cx_Oracle
import sys
import datetime

class sql():
	def __init__(self):
		self.connection = cx_Oracle.connect('arbit/arbit@orcl')		
		
	def create_table(self):	
		cursor = self.connection.cursor()
		sql = 'CREATE TABLE Form4(SecDocument varchar(37), AcceptanceDatetime timestamp, IssuerTradingSymbol varchar(10), RptOwnerCik varchar(10), RptOwnerName varchar(21), IsDirector varchar(1), IsOfficer varchar(1), IsTenPercentOwner varchar(1), IsOther varchar(1), TransactionDate date, TransactionShares float, TransactionPricePerShare float, TransactionAcquiredDisposed varchar(1), SharesOwned float, CONSTRAINT Form4PK PRIMARY KEY (SecDocument))'
		
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
		sql = 'DROP TABLE Form4'
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
		transactionDate = datetime.date(year, month, day)

		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO Form4(SecDocument, AcceptanceDatetime, IssuerTradingSymbol, RptOwnerCik, RptOwnerName, IsDirector, IsOfficer, IsTenPercentOwner, IsOther, TransactionDate, TransactionShares, TransactionPricePerShare, TransactionAcquiredDisposed, SharesOwned) VALUES (:SecDocument, :AcceptanceDatetime, :IssuerTradingSymbol, :RptOwnerCik, :RptOwnerName, :IsDirector, :IsOfficer, :IsTenPercentOwner, :IsOther, :TransactionDate, :TransactionShares, :TransactionPricePerShare, :TransactionAcquiredDisposed, :SharesOwned)",
			{
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
		)
		self.connection.commit()
		cursor.close()
		
	def fetch(self, currentDate):			
		cursor = self.connection.cursor()
		
		cursor.execute("SELECT * FROM form4 where form4.AcceptanceDatetime>=:StartDate and form4.AcceptanceDatetime<:EndDate and form4.transactionacquireddisposed='A'",
			StartDate = currentDate,
			EndDate = currentDate + datetime.timedelta(days=1),
		)	
	
		rows = cursor.fetchall()
		
		if not rows:
			return None
				
		forms = []
		for row in rows:
			form = {}
			form['SecDocument'] = row[0]
			form['AcceptanceDatetime'] = row[1] 
			form['IssuerTradingSymbol'] = row[2] 
			form['RptOwnerCik'] = row[3]
			form['RptOwnerName'] = row[4] 
			form['IsDirector'] = row[5]
			form['IsOfficer'] = row[6]
			form['IsTenPercentOwner'] = row[7] 
			form['IsOther'] = row[8]
			form['TransactionDate'] = row[9]
			form['TransactionShares'] = row[10]
			form['TransactionPricePerShare'] = row[11]
			form['TransactionAcquiredDisposed'] = row[12]
			form['SharesOwned'] = row[13]
			forms.append(form)
			
		cursor.close()	
		
		return forms
