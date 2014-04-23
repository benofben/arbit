import boto.dynamodb2
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table

def createTable():
	Table.create('symbols', schema=[HashKey('symbol'),])

def dropTable():
	try:
		symbols = Table('symbols')
		symbols.delete()
	except boto.exception.JSONResponseError as e:
		# probably means the table doesn't exist
		print(e)
	
def insert(symbol):
		symbols = Table('symbols')
		symbols.put_item(data={'symbol': symbol})
		
def batchInsert(symbolInformation):
		symbols = Table('symbols')
		with symbols.batch_write() as batch:
			for symbol in symbolInformation:
				batch.put_item(data={'symbol': symbol})