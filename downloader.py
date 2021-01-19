import os
import shutil
import http.client
import datetime
import constants


def run():
    delete()
    download()
    reformat()


def delete():
    if os.path.exists(constants.dataDirectory + 'quotes'):
        shutil.rmtree(constants.dataDirectory + 'quotes')
    os.makedirs(constants.dataDirectory + 'quotes')


def download():
    symbols = 'F', 'COP'
    for symbol in symbols:
        downloadSymbol(symbol)


def downloadSymbol(symbol):
    print('Downloading historical data for ' + symbol + '...')

    '''
    A yahoo URL looks like this:
    https://query1.finance.yahoo.com/v7/finance/download/COP?period1=378604800&period2=1610928000&interval=1d&events=history

    The time period uses a UNIX epoch.
    '''

    period1 = str(int(datetime.datetime(2010, 1, 1).timestamp()))
    period2 = str(int(datetime.datetime.today().timestamp()))

    conn = http.client.HTTPSConnection('query1.finance.yahoo.com')
    conn.request('GET', '/v7/finance/download/' + symbol + '?period1=' + period1 + '&period2=' + period2 + '&interval=1d&events=history')
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
        symbol = inputFilename.replace('.csv', '')
        reformatSymbol(inputFile, outputFile, symbol)
        inputFile.close()

    outputFile.close()
    print('Done reformating quotes')


def reformatSymbol(inputFile, outputFile, symbol):
    for line in inputFile:
        if line.startswith('Date'):
            # Then this is a header line
            pass
        else:
            outputFile.write(symbol + ',' + line)
