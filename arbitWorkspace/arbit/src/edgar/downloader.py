import ftplib
import datetime
import constants
import os
import gzip

def run():
	ftp = ftplib.FTP('sec.gov')
	ftp.login()

	directoryNames = getDirectoryNames()
	
	masterFilenames = []
	for directoryName in directoryNames:
		masterFilenames += getMasterFilenames(ftp, directoryName)
	
	downloadMasterFiles(ftp, masterFilenames)
	
	masterFilenames = os.listdir(constants.dataDirectory + 'edgar/masterFiles/')
	masterFilenames.reverse() # we want to do the newest ones first
	
	form4Filenames = []
	for masterFilename in masterFilenames:
		form4Filenames += parseForm4FilenamesFromMasterFile(constants.dataDirectory + 'edgar/masterFiles/' + masterFilename)
	
	downloadForm4Files(ftp, form4Filenames)
			
	ftp.quit()

def parseForm4FilenamesFromMasterFile(filename):
	form4Filenames = []
	
	fileExtension = filename.split('.')
	fileExtension = fileExtension[len(fileExtension)-1]
	
	if fileExtension == 'idx':
		pass
	elif fileExtension == 'gz':
		plainTextFilename = str.replace(filename, '.idx.gz', '.idx')
		
		if os.path.exists(plainTextFilename):
			# we already created a gunzipped version of this file and will read it later
			return []
		else:		 
			#read the gzipped file in
			file = gzip.open(filename, 'r')
			content = file.read()
			file.close()
			
			# write the content to a plain text file 
			outputFile = open(plainTextFilename, 'wb')
			outputFile.write(content)
			outputFile.close()
			
			filename=plainTextFilename
		
	file = open(filename, 'r')
	for line in file:
		splitLine = line.split('|')
		if len(splitLine)!=5:
			pass
		elif splitLine[0]=='CIK':
			pass
		else:
			if splitLine[2]=='4':
				form4Filenames.append(splitLine[4].strip())	
	file.close()
	
	return form4Filenames

def getDirectoryNames():
	directoryNames = []
	directoryNames.append('/edgar/daily-index/master.*')
	
	# this goes back to 1994.  The masterfile naming conventions change over the years which is 
	# probably why the SEC puts these in their own directories.
	# Let's do 2012 for now and then figure out how to deal with the rest later.
	for year in range(datetime.datetime.now().year, 2012-1, -1):
		for quarter in ['QTR4','QTR3','QTR2','QTR1']:
			directoryNames.append('/edgar/daily-index/' + str(year) + '/' + quarter + '/master.*')
		
	return directoryNames

def getMasterFilenames(ftp, directoryName):
	masterFilenames = []
	
	try:
		masterFilenames = ftp.nlst(directoryName)
		print('Downloaded master filenames for ' + directoryName + '.')
	except:
		print('Could not download master filenames for ' + directoryName + '.')
	
	return masterFilenames

def downloadMasterFiles(ftp, filenames):
	downloadDirectoryName = constants.dataDirectory + 'edgar/masterFiles/'
	if not os.path.exists(downloadDirectoryName):
		os.makedirs(downloadDirectoryName)
	
	for filename in filenames:
		downloadFilename = filename.split('/')
		downloadFilename = downloadFilename[len(downloadFilename)-1]
		downloadFilename = downloadDirectoryName + downloadFilename
		
		if not os.path.exists(downloadFilename) and not os.path.exists(str.replace(downloadFilename,'.idx.gz','.idx')):
			print('Downloading master file ' + filename + '.')
			ftp.retrbinary('RETR ' + filename, open(downloadFilename, 'wb').write)
		else:
			print('Skipping existing file ' + filename + '.')

def downloadForm4Files(ftp, filenames):
	numberOfFilesRemaining = len(filenames) 
	
	downloadDirectoryName = constants.dataDirectory + 'edgar/'
	if not os.path.exists(downloadDirectoryName):
		os.makedirs(downloadDirectoryName)
	
	for filename in filenames:
		downloadFilename = filename.split('/')
		
		downloadDirectoryName = constants.dataDirectory + downloadFilename[0]+ '/'+ downloadFilename[1]+ '/'+ downloadFilename[2]+ '/'
		if not os.path.exists(downloadDirectoryName):
			os.makedirs(downloadDirectoryName)		
		
		downloadFilename = downloadFilename[3]
		downloadFilename = downloadDirectoryName + downloadFilename
		
		if os.path.exists(downloadFilename):
			print('Skipping existing form 4 file ' + filename + ', ' + str(numberOfFilesRemaining) + ' files remaining.')
		else:
			try:
				ftp.retrbinary('RETR ' + filename, open(downloadFilename, 'wb').write)
				print('Downloaded form 4 file ' + filename + ', ' + str(numberOfFilesRemaining) + ' files remaining.')
			except:
				print('Failed to download form 4 file ' + filename + ', ' + str(numberOfFilesRemaining) + ' files remaining.')
		numberOfFilesRemaining-=1