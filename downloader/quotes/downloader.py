import os
import shutil
import http.client
import datetime
import constants
import symbols.database
import quotes.database


def run():
    #delete()
    #download()
    reformat()
    upload()


def delete():
    if os.path.exists(constants.dataDirectory + 'quotes'):
        shutil.rmtree(constants.dataDirectory + 'quotes')
    os.makedirs(constants.dataDirectory + 'quotes')


def download():
    db = symbols.database.database()
    s = db.getSymbols()
    for symbol in s:
        downloadSymbol(symbol)


def downloadSymbol(symbol):
    print('Downloading historical data for ' + symbol + '...')
    conn = http.client.HTTPConnection('ichart.finance.yahoo.com')

    '''
    Notes on the yahoo parameters:
    d=end month-1
    e=end day
    f=end year
    g=d?
    a=start month-1 (0 = January)
    b=start day (2)
    c=start year (2002)
    '''

    today = datetime.date.today()
    endYear = today.strftime('%Y')
    endMonth = str(int(today.strftime('%m')) - 1)
    endDay = today.strftime('%d')

    startYear = '2002'
    startMonth = '0'
    startDay = '1'

    conn.request('GET', '/table.csv?s=' + symbol + '&d=' + endMonth + '&e=' + endDay + '&f=' + endYear + '&g=d&a=' + startMonth + '&b=' + startDay + '&c=' + startYear + '&ignore=.csvc')
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    conn.close()
    if response.status == 200 and response.reason == 'OK':
        data = data.decode('windows-1252')
        outputFilename = constants.dataDirectory + 'quotes/' + symbol + '.csv'
        outputFile = open(outputFilename, 'w')
        outputFile.write(data)
        outputFile.close()
        print('Saved historical data for ' + symbol + '.\n')
    else:
        print('Download failed for symbol ' + symbol + '.\n')
        return False
    return True


def reformat():
    print('Reformating the quotes...')
    outputFilename = constants.dataDirectory + 'quotes.csv'
    outputFile = open(outputFilename, 'w')

    path = constants.dataDirectory + 'quotes/'
    inputFilenames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for inputFilename in inputFilenames:
        inputFile = open(path + inputFilename, 'r')
        reformatSymbol(inputFile, outputFile)
        inputFile.close()

    outputFile.close()


def reformatSymbol(inputFile, outputFile):
    for line in inputFile:
        if line.startswith('Date'):
            # Then this is a header line
            print('skipped line')
        else:
            outputFile.write(line)


def upload():
    print('Writing quotes to the database...')
    db = quotes.database.database()
    db.delete()
    db.create()
    db.upload(constants.dataDirectory + 'quotes.csv')
    print('Done uploading quotes to the database')
