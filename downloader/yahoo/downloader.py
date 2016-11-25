import os
import shutil
import http.client
import constants
import nasdaq.database
import yahoo.database


def run():
    delete()
    download()
    load()


def delete():
    if os.path.exists(constants.dataDirectory + 'quotes'):
        shutil.rmtree(constants.dataDirectory + 'quotes')
    os.makedirs(constants.dataDirectory + 'quotes')


def download():
    symbolsDB = nasdaq.database.database()
    symbols = symbolsDB.getSymbols()

    outputFilename = constants.dataDirectory + 'quotes/quotes.csv'
    outputFile = open(outputFilename, 'w')

    for symbol in symbols:
        if downloadSymbol(symbol):
            reformat(symbol, outputFile)

    outputFile.close()


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
        save(data, symbol)
        print('Saved historical data for ' + symbol + '.\n')
    else:
        print('Download failed for symbol ' + symbol + '.\n')
        return False
    return True


def save(data, symbol):
    filename = constants.dataDirectory + 'quotes/' + symbol + '.csv'
    file = open(filename, 'w')
    file.write(data)
    file.close()


def reformat(symbol, outputFile):
    inputFilename = constants.dataDirectory + 'quotes/' + symbol + '.csv'
    inputFile = open(inputFilename, 'r')
    for line in inputFile:
        if line.startswith('Date'):
            # Then this is a header line
            print('skipped line')
        else:
            outputFile.write(line)
    inputFile.close()


def load():
    quotesDB = yahoo.database.database()
    quotesDB.delete()
    quotesDB.upload(constants.dataDirectory + 'quotes/quotes.csv')
