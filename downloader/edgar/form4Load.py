import edgar.downloader
import edgar.form4
import edgar.database
import os
import constants


# This reads all form 4 files from the local filesystem and writes them to the database.
# In most cases, downloaderEDGAR could be run instead.  
# This only needs to be run if that job was killed part way through.

def run():
    form4DB = edgar.database.database()

    masterFilenames = os.listdir(constants.dataDirectory + 'edgar/masterFiles/')
    masterFilenames.reverse()  # we want to do the newest ones first

    form4Filenames = []
    for masterFilename in masterFilenames:
        print(masterFilename)
        form4Filenames += edgar.downloader.parseForm4FilenamesFromMasterFile(
            constants.dataDirectory + 'edgar/masterFiles/' + masterFilename)

    for filename in form4Filenames:
        filename = constants.dataDirectory + filename
        print('Parsing 4 Form file ' + filename)
        transactions = edgar.form4.parse(filename)
        for transaction in transactions:
            form4DB.insert(transaction)


run()
