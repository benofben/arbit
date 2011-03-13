import cx_Oracle
import constants
import sys
import datetime

class sql():
	def __init__(self):
		self.connection = cx_Oracle.connect('arbit/arbit@orcl')		
		
	def create_table(self):	
		cursor = self.connection.cursor()
		sql = 'CREATE TABLE TrainingPoints(Outcome varchar(8), High float, Low float, Close float, Volume float, TrainingDate date, PWin float, Symbol varchar(8), Exchange varchar(6), IPOYear number(4), Sector varchar(21), Industry varchar(62), MarketCap number(14,2), CONSTRAINT TrainingPointsPK PRIMARY KEY (Symbol, Exchange, TrainingDate))'
		
		try:	
			response = cursor.execute(sql)
			print(response)
		except cx_Oracle.DatabaseError as exc:
			error, = exc.args
			print(sys.stderr, "Oracle-Error-Code:", error.code)
			print(sys.stderr, "Oracle-Error-Message:", error.message)
		self.connection.commit()
		cursor.close()
	
	def createClassificationTable(self):	
		cursor = self.connection.cursor()
		sql = 'CREATE TABLE Classification(Classification float, Symbol varchar(8), CurrentTestDate date, Outcome varchar(8), High float, Close float, CONSTRAINT ClassificationPK PRIMARY KEY (Classification, Symbol, CurrentTestDate, Outcome))'
				
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
		sql = 'DROP TABLE TrainingPoints'
		try:	
			response = cursor.execute(sql)
			print(response)
		except cx_Oracle.DatabaseError as exc:
			error, = exc.args
			print(sys.stderr, "Oracle-Error-Code:", error.code)
			print(sys.stderr, "Oracle-Error-Message:", error.message)
		self.connection.commit()
		cursor.close()

	def dropClassificationTable(self):
		cursor = self.connection.cursor()
		sql = 'DROP TABLE Classification'
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

	def insert(self, trainingPoint):	
		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO TrainingPoints(Outcome,High,Low,Close,Volume,TrainingDate,PWin,Symbol,Exchange,IPOYear,Sector,Industry,MarketCap) VALUES (:Outcome,:High,:Low,:Close,:Volume,:TrainingDate,:PWin,:Symbol,:Exchange,:IPOYear,:Sector,:Industry,:MarketCap)",
			{
				'Outcome' : trainingPoint['Outcome'],
				'High' : trainingPoint['High'],
				'Low' : trainingPoint['Low'],
				'Close' : trainingPoint['Close'],
				'Volume' : trainingPoint['Volume'],
				'TrainingDate' : trainingPoint['Date'],
				'PWin' : trainingPoint['PWin'],
				'Symbol' : trainingPoint['Symbol'],
				'Exchange' : trainingPoint['Exchange'],
				'IPOYear' : trainingPoint['IPOYear'],
				'Sector' : trainingPoint['Sector'],
				'Industry' : trainingPoint['Industry'],
				'MarketCap' : trainingPoint['MarketCap'],
			}
		)
		self.connection.commit()
		cursor.close()
		
	def fetchTrainingPoints(self, currentDate):
		cursor = self.connection.cursor()
		
		cursor.execute("SELECT Outcome,High,Low,Close,Volume,TrainingDate,PWin,Symbol,Exchange,IPOYear,Sector,Industry,MarketCap FROM TrainingPoints WHERE TrainingDate BETWEEN :StartDate AND :CurrentDate",
			StartDate = constants.startDate,
			CurrentDate = currentDate
		)
		
		trainingInformation = {}
		trainingInformation['Outcome']=[]
		trainingInformation['High']=[]
		trainingInformation['Low']=[]
		trainingInformation['Close']=[]
		trainingInformation['Volume']=[]
		trainingInformation['TrainingDate']=[]
		trainingInformation['PWin']=[]
		trainingInformation['Symbol']=[]
		trainingInformation['Exchange']=[]
		trainingInformation['IPOYear']=[]
		trainingInformation['Sector']=[]
		trainingInformation['Industry']=[]
		trainingInformation['MarketCap']=[]

		rows = cursor.fetchall()
		if not rows:
			return None
		
		for row in rows:
			trainingInformation['Outcome'].append(row[0])
			trainingInformation['High'].append(row[1])
			trainingInformation['Low'].append(row[2])
			trainingInformation['Close'].append(row[3])
			trainingInformation['Volume'].append(row[4])
			trainingInformation['TrainingDate'].append(row[5])
			trainingInformation['PWin'].append(row[6])
			trainingInformation['Symbol'].append(row[7])
			trainingInformation['Exchange'].append(row[8])
			trainingInformation['IPOYear'].append(row[9])
			trainingInformation['Sector'].append(row[10])
			trainingInformation['Industry'].append(row[11])
			trainingInformation['MarketCap'].append(row[12])
		cursor.close()
		
		return trainingInformation
	
	def fetchTestPoint(self, symbol, currentDate):
		cursor = self.connection.cursor()
		
		cursor.execute("SELECT Outcome,High,Low,Close,Volume,TrainingDate,PWin,Symbol,Exchange,IPOYear,Sector,Industry,MarketCap FROM TrainingPoints WHERE Symbol=:symbol AND TrainingDate BETWEEN :StartDate AND :CurrentDate",
			Symbol = symbol, 
			StartDate = constants.startDate,
			CurrentDate = currentDate
		)
		
		trainingInformation = {}
		trainingInformation['Outcome']=[]
		trainingInformation['High']=[]
		trainingInformation['Low']=[]
		trainingInformation['Close']=[]
		trainingInformation['Volume']=[]
		trainingInformation['TrainingDate']=[]
		trainingInformation['PWin']=[]
		trainingInformation['Symbol']=[]
		trainingInformation['Exchange']=[]
		trainingInformation['IPOYear']=[]
		trainingInformation['Sector']=[]
		trainingInformation['Industry']=[]
		trainingInformation['MarketCap']=[]

		rows = cursor.fetchall()
		if not rows:
			return None
		
		for row in rows:
			trainingInformation['Outcome'].append(row[0])
			trainingInformation['High'].append(row[1])
			trainingInformation['Low'].append(row[2])
			trainingInformation['Close'].append(row[3])
			trainingInformation['Volume'].append(row[4])
			trainingInformation['TrainingDate'].append(row[5])
			trainingInformation['PWin'].append(row[6])
			trainingInformation['Symbol'].append(row[7])
			trainingInformation['Exchange'].append(row[8])
			trainingInformation['IPOYear'].append(row[9])
			trainingInformation['Sector'].append(row[10])
			trainingInformation['Industry'].append(row[11])
			trainingInformation['MarketCap'].append(row[12])
		cursor.close()
		
		return trainingInformation

	def insertClassification(self, classification):
		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO Classification(Classification, Symbol, CurrentTestDate, Outcome, High, Close) VALUES (:Classification, :Symbol, :CurrentTestDate, :Outcome, :High, :Close)",
			{
				'Classification' : classification['Classification'],
				'Symbol' : classification['Symbol'],
				'CurrentTestDate' : classification['CurrentTestDate'],
				'Outcome' : classification['Outcome'],
				'High' : classification['High'],
				'Close' : classification['Close'],
			}
		)
		self.connection.commit()
		cursor.close()

	def fetchClassifications(self):
		classifications = {}
		classifications['Classification']=[]
		classifications['Symbol']=[]
		classifications['CurrentTestDate']=[]
		classifications['Outcome']=[]
		classifications['High']=[]
		classifications['Close']=[]
		
		cursor = self.connection.cursor()
		
		currentTestDate = constants.startDate
		while currentTestDate < constants.endDate:
			# need to find the symbol with the maximum confidence for this date
			
			cursor.execute("SELECT MAX(Classification) FROM Classification WHERE CurrentTestDate=:currentTestDate",			 
				CurrentTestDate = currentTestDate
			)
			rows = cursor.fetchall()
			if rows:
				if rows[0]:
					classification = rows[0][0]

					# Now get the data for this classification score
					cursor.execute("SELECT Classification, Symbol, CurrentTestDate, Outcome, High, Close FROM Classification WHERE Classification=:classification",			 
						Classification = classification,
					)
					
					rows = cursor.fetchall()
					for row in rows:
						classifications['Classification'].append(row[0])
						classifications['Symbol'].append(row[1])
						classifications['CurrentTestDate'].append(row[2])
						classifications['Outcome'].append(row[3])
						classifications['High'].append(row[4])
						classifications['Close'].append(row[5])
			currentTestDate = currentTestDate + datetime.timedelta(days=1)
		return classifications