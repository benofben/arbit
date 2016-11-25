import os
import shutil
import datetime
import http.client
import csv
import constants
import nasdaq.database
#import yahoo.database


def run():
    delete()

    failedSymbolsFilename = constants.dataDirectory + 'yahoo/failedQuotesSymbols.txt'
    failedSymbolsFile = open(failedSymbolsFilename, 'w')

    #quotesDB = yahoo.database.database()
    #quotesDB.dropCollection()

    symbolsDB = nasdaq.database.database()
    symbols = symbolsDB.getSymbols()
    while symbols:
        print(str(len(s)) + ' symbols remaining.')
        symbol = symbols.pop()
        if not download(symbol):
            failedSymbolsFile.write(symbol + '\n')
        else:
            quotes = loadQuotesFromDisk(symbol)
            quotes['Symbol'] = symbol
            #quotesDB.insert(quotes)

    failedSymbolsFile.close()


def delete():
    if os.path.exists(constants.dataDirectory + 'yahoo/quotes'):
        shutil.rmtree(constants.dataDirectory + 'yahoo/quotes')
    os.makedirs(constants.dataDirectory + 'yahoo/quotes/')


def download(symbol):
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
        reformatAndSaveQuotes(data, symbol)
        print('Saved historical data for ' + symbol + '.\n')
    else:
        print('Download failed for symbol ' + symbol + '.\n')
        return False
    return True


def reformatAndSaveQuotes(data, symbol):
    quotes = []
    lines = data.split('\n')
    i = 0
    for line in lines:
        if (i > 0):
            quotes.append(line)
        i = i + 1

    # we want the list to go from oldest quote to newest
    quotes.reverse()

    filename = constants.dataDirectory + 'yahoo/quotes/' + symbol + '.csv'
    file = open(filename, 'w')
    i = 0
    for line in quotes:
        if (i > 0):
            file.write(line + '\n')
        i = i + 1
    file.close()


def loadQuotesFromDisk(symbol):
    inputFilename = constants.dataDirectory + 'yahoo/quotes/' + symbol + '.csv'
    inputFile = open(inputFilename, 'r')

    quotes = {}
    quotes['Date'] = []
    quotes['Open'] = []
    quotes['High'] = []
    quotes['Low'] = []
    quotes['Close'] = []
    quotes['Volume'] = []
    quotes['AdjClose'] = []

    reader = csv.reader(inputFile)

    for Date, Open, High, Low, Close, Volume, AdjClose in reader:
        dt = Date.split('-')
        Date = datetime.date(int(dt[0]), int(dt[1]), int(dt[2]))

        quotes['Date'].append(Date)
        quotes['Open'].append(float(Open))
        quotes['High'].append(float(High))
        quotes['Low'].append(float(Low))
        quotes['Close'].append(float(Close))
        quotes['Volume'].append(int(Volume))
        quotes['AdjClose'].append(float(AdjClose))

    inputFile.close()
    return quotes
