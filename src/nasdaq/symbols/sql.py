import cx_Oracle

class sql():
	def __init__(self):
		self.connection = cx_Oracle.connect('arbit/arbit@orcl')
	
	def __del__(self):
		self.connection.close()

	def insert(self):
		pass
		'''
		sql = str('INSERT INTO prime.utwsLOT VALUES (' + str(self.kID) + ',' + string)
		cursor = self.connection.cursor()
		cursor.execute(sql)
		'''


