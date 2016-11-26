import os
import shutil
import http.client
import csv
import constants
import symbols.database

# Options are: NYSE, NASDAQ, AMEX
exchanges = ['NYSE', 'NASDAQ']


def run():
    delete()
    download()
    reformat()
    load()


def delete():
    if os.path.exists(constants.dataDirectory + 'symbols'):
        shutil.rmtree(constants.dataDirectory + 'symbols')
    os.makedirs(constants.dataDirectory + 'symbols')


def download():
    for exchange in exchanges:
        downloadExchange(exchange)


def downloadExchange(exchange):
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


def reformat():
    for exchange in exchanges:
        reformatExchange(exchange)


def reformatExchange(exchange):
    inputFile = open(constants.dataDirectory + 'symbols/' + exchange + '.csv', 'r')
    reader = csv.reader(inputFile)

    outputFile = open(constants.dataDirectory + 'symbols/' + exchange + '.reformat.csv', 'w')
    writer = csv.writer(outputFile)

    for Symbol, Name, LastSale, MarketCap, unused_ADRTSO, IPOyear, Sector, Industry, unused_SummaryQuote, unused_Null in reader:
        if (Symbol == 'Symbol'):
            # Then this is the first line
            pass
        else:
            Symbol = Symbol.replace('^', '.')
            Symbol = Symbol.replace('/', '.')
            Symbol = Symbol.strip()

            if (LastSale == 'n/a'):
                LastSale = 0

            if (not IPOyear.isdigit()):
                IPOyear = 0

        writer.writerow([exchange, Symbol, Name, LastSale, MarketCap, IPOyear, Sector, Industry])

    inputFile.close()
    outputFile.close()


def load():
    print('Writing symbols to the database...')

    db = symbols.database.database()
    #db.delete()
    db.create()

    for exchange in exchanges:
        filename = constants.dataDirectory + 'symbols/' + exchange + '.reformat.csv'
        print(filename)
        assert os.path.exists(filename)
        db.upload(filename)

    print('Loaded ' + str(len(db.getSymbols())) + ' into the database')
