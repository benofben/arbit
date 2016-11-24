import constants
import nasdaq.database
import os
import shutil
import http.client
import csv

# Options are: NYSE, NASDAQ, AMEX
exchanges = ['NYSE', 'NASDAQ']


def downloadSymbols():
    if os.path.exists(constants.dataDirectory + 'symbols'):
        shutil.rmtree(constants.dataDirectory + 'symbols')
    os.makedirs(constants.dataDirectory + 'symbols')

    for exchange in exchanges:
        downloadSymbols(exchange)


def downloadSymbols(exchange):
    print('Trying to get exchange ' + exchange + '...')
    conn = http.client.HTTPConnection('www.nasdaq.com')
    conn.request('GET', '/screening/companies-by-industry.aspx?exchange=' + exchange + '&render=download')
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    conn.close()

    print('Done downloading.  Writing to file.\n')
    file = open(constants.dataDirectory + 'symbols/' + exchange + '.csv', 'w')
    data = data.decode()
    file.write(data)
    file.close()


def readSymbolInformation():
    symbols=[]
    for exchange in exchanges:
        symbolInformation = readSymbolInformation(exchange)
        for symbol in symbolInformation:
            symbols.append(symbolInformation[symbol])
    return symbols


def readSymbolInformation(exchange):
    symbolInformation = {}
    inputFile = open(constants.dataDirectory + 'symbols/' + exchange + '.csv', 'r')
    reader = csv.reader(inputFile)

    for Symbol, Name, LastSale, MarketCap, unused_ADRTSO, IPOyear, Sector, Industry, unused_SummaryQuote, unused_Null in reader:
        if (Symbol == 'Symbol'):
            # Then this is the first line
            pass
        else:
            Symbol = Symbol.replace('^', '.')
            Symbol = Symbol.replace('/', '.')

            symbolInformation[Symbol] = {}
            symbolInformation[Symbol]['Symbol'] = Symbol
            symbolInformation[Symbol]['Exchange'] = exchange
            symbolInformation[Symbol]['Name'] = Name
            if (LastSale == 'n/a'):
                LastSale = 0
            symbolInformation[Symbol]['LastSale'] = float(LastSale)
            symbolInformation[Symbol]['MarketCap'] = float(MarketCap)
            if (not IPOyear.isdigit()):
                IPOyear = 0
            symbolInformation[Symbol]['IPOYear'] = IPOyear
            symbolInformation[Symbol]['Sector'] = Sector
            symbolInformation[Symbol]['Industry'] = Industry

    inputFile.close()
    return symbolInformation


def loadSymbolsIntoDB():

    db = nasdaq.database.database()
    db.insert()

    print('Inserted symbols into database.')
    print(db.getSymbols())


def run():
    downloadSymbols()
    loadSymbolsIntoDB()
