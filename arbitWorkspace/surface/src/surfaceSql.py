import cx_Oracle
import sys

class sql():
	def __init__(self):
		self.connection = cx_Oracle.connect('arbit/arbit@orcl')
	
	def create_table(self):
		# Data points look like
		# Outcome, Pwin(window), window
		
		cursor = self.connection.cursor()		
		sql = 'CREATE TABLE Surface(Window int, Pwin float, Outcome float)'
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
		sql = 'DROP TABLE Surface'
		try:		
			response = cursor.execute(sql)
			print(response)
		except cx_Oracle.DatabaseError as exc:
			error, = exc.args
			print(sys.stderr, "Oracle-Error-Code:", error.code)
			print(sys.stderr, "Oracle-Error-Message:", error.message)
		self.connection.commit()
		cursor.close()

	def insert(self, points):	
		cursor = self.connection.cursor()
		
		for key in points:			
			cursor.execute("INSERT INTO Surface(Outcome, Pwin, Window) VALUES (:Outcome, :Pwin, :Window)",
				{
					'Outcome' : points[key]['Outcome'],
					'Pwin' : points[key]['Pwin'],
					'Window' : points[key]['Window'],
				}
			)
		self.connection.commit()
		cursor.close()

	def __del__(self):
		self.connection.close()
	