def GetAllQuotes():
    symbols = GetSymbols()
    q = {}
    for symbol in symbols:
        print "Loading symbol " + symbol + "."
        q[symbol] = GetQuotes(symbol)
    return q


def GetQuotes(symbol):
    inputFilename = "data/reformattedQuotes/" + symbol + ".csv"
    inputFile=open(inputFilename, 'rb')

    import csv
    reader = csv.reader(inputFile)

    quotes = []
    for Date, Open, High, Low, Close, Volume, AdjClose in reader:
        quotes.append([Date, Open, High, Low, Close, Volume, AdjClose])

    inputFile.close()
    return quotes

def GetSymbols():
    dirname = "data/reformattedQuotes"
    symbols=[]
    import os
    files=os.listdir(dirname)
    for file in files:
        symbols.append(file.replace('.csv',''))
    return symbols
