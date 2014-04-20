import edgar.downloader
import edgar.form4
import edgar.sql
import os
import constants

# This reads all form 4 files from the local filesystem and writes them to the database.  In most cases, downloaderEDGAR could be run instead.  This only needs to be run if that job was killed part way through.

def run():
	mySql = edgar.sql.sql()
	#mySql.drop_table()
	#mySql.create_table()

	masterFilenames = os.listdir(constants.dataDirectory + 'edgar/masterFiles/')
	masterFilenames.reverse() # we want to do the newest ones first
	
	form4Filenames = []
	for masterFilename in masterFilenames:
		form4Filenames += edgar.downloader.parseForm4FilenamesFromMasterFile(constants.dataDirectory + 'edgar/masterFiles/' + masterFilename)

	for filename in form4Filenames:	
		filename = constants.dataDirectory + filename
		print('Parsing 4 Form file ' + filename)
		transactions = edgar.form4.parse(filename)
		for transaction in transactions:
			try:
				mySql.insert(transaction)
			except:
				print('Duplicate record')

run()