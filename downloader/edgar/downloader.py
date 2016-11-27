import ftplib
import datetime
import constants
import os
import gzip
import edgar.form4
import edgar.database


def run():
    ftp = ftplib.FTP('ftp.sec.gov')
    ftp.login()

    db = edgar.database.database()
    db.create()

    directoryNames = getDirectoryNames()

    masterFilenames = []
    for directoryName in directoryNames:
        masterFilenames += getMasterFilenames(ftp, directoryName)

    for masterFilename in masterFilenames:
        downloadMasterFile(ftp, masterFilename)
        masterFilename = masterFilename.split('/')
        masterFilename = masterFilename[len(masterFilename) - 1]
        form4Filenames = parseForm4FilenamesFromMasterFile(
            constants.dataDirectory + 'edgar/masterFiles/' + masterFilename)

        for form4Filename in form4Filenames:
            downloadForm4File(ftp, form4Filename)
            form4Filename = constants.dataDirectory + form4Filename
            if os.path.exists(form4Filename):
                print('Parsing Form 4 file ' + form4Filename)
                transactions = edgar.form4.parse(form4Filename)
                for transaction in transactions:
                    db.insert(transaction)
            else:
                print('Failed to download Form 4 file ' + form4Filename)

    ftp.quit()


def parseForm4FilenamesFromMasterFile(filename):
    form4Filenames = []

    fileExtension = filename.split('.')
    fileExtension = fileExtension[len(fileExtension) - 1]

    if fileExtension == 'idx':
        pass
    elif fileExtension == 'gz':
        plainTextFilename = str.replace(filename, '.idx.gz', '.idx')

        if os.path.exists(plainTextFilename):
            # we already created a gunzipped version of this file and will read it later
            return []
        else:
            # read the gzipped file in
            file = gzip.open(filename, 'r')
            content = file.read()
            file.close()

            # write the content to a plain text file
            outputFile = open(plainTextFilename, 'wb')
            outputFile.write(content)
            outputFile.close()

            filename = plainTextFilename

    file = open(filename, encoding='ISO-8859-1')
    for line in file:
        splitLine = line.split('|')
        if len(splitLine) != 5:
            pass
        elif splitLine[0] == 'CIK':
            pass
        else:
            if splitLine[2] == '4':
                form4Filenames.append(splitLine[4].strip())
    file.close()

    return form4Filenames


def getDirectoryNames():
    directoryNames = []
    directoryNames.append('/edgar/daily-index/master.*')

    # this goes back to 1994.  The masterfile naming conventions change over the years which is
    # probably why the SEC puts these in their own directories.
    # Let's do 2012 for now and then figure out how to deal with the rest later.
    for year in range(datetime.datetime.now().year, 2012 - 1, -1):
        for quarter in ['QTR4', 'QTR3', 'QTR2', 'QTR1']:
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


def downloadMasterFile(ftp, filename):
    downloadDirectoryName = constants.dataDirectory + 'edgar/masterFiles/'
    if not os.path.exists(downloadDirectoryName):
        os.makedirs(downloadDirectoryName)

    downloadFilename = filename.split('/')
    downloadFilename = downloadFilename[len(downloadFilename) - 1]
    downloadFilename = downloadDirectoryName + downloadFilename

    if not os.path.exists(downloadFilename) and not os.path.exists(str.replace(downloadFilename, '.idx.gz', '.idx')):
        print('Downloading master file ' + filename + '.')
        ftp.retrbinary('RETR ' + filename, open(downloadFilename, 'wb').write)
    else:
        print('Skipping existing master file ' + filename + '.')


def downloadForm4File(ftp, filename):
    downloadFilename = filename.split('/')
    downloadDirectoryName = constants.dataDirectory + downloadFilename[0] + '/' + downloadFilename[1] + '/' + downloadFilename[2] + '/'
    if not os.path.exists(downloadDirectoryName):
        os.makedirs(downloadDirectoryName)
    downloadFilename = downloadFilename[3]
    downloadFilename = downloadDirectoryName + downloadFilename

    if os.path.exists(downloadFilename):
        raise Exception('Skipping existing form 4 file ' + filename)
    else:
        try:
            ftp.retrbinary('RETR ' + filename, open(downloadFilename, 'wb').write)
            print('Downloaded form 4 file ' + filename)
        except:
            raise Exception('Failed to download form 4 file ' + filename)
