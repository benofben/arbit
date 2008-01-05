def getAllQuotes():
    symbols=getSymbols()
    quotes={}
    for symbol in symbols:
        print 'Loading symbol ' + symbol + '.'
        quotes[symbol]=getQuotes(symbol)
    return quotes

def getQuotes(symbol):
    inputFilename='data/quotes/' + symbol + '.csv'
    inputFile=open(inputFilename, 'rb')

    quotes={}
    quotes['Date']=[]
    quotes['Open']=[]
    quotes['High']=[]
    quotes['Low']=[]
    quotes['Close']=[]
    quotes['Volume']=[]
    quotes['AdjClose']=[]
    
    import datetime
    import csv
    reader=csv.reader(inputFile)

    for Date, Open, High, Low, Close, Volume, AdjClose in reader:
        dt=Date.split('-')
        Date=datetime.date(int(dt[0]), int(dt[1]), int(dt[2]))

        quotes['Date'].append(Date)
        quotes['Open'].append(float(Open))
        quotes['High'].append(float(High))
        quotes['Low'].append(float(Low))
        quotes['Close'].append(float(Close))
        quotes['Volume'].append(long(Volume))
        quotes['AdjClose'].append(float(AdjClose))
        
    inputFile.close()
    return quotes

def getSymbols():
    dirname='data/quotes/'
    symbols=[]
    import os
    files=os.listdir(dirname)
    for file in files:
        symbols.append(file.replace('.csv', ''))
    return symbols

# returns the index of the quote for the given date for quotes[symbol]
def getIndex(date, quotes):
    try:
        return quotes['Date'].index(date)
    except ValueError:
        return False

# returns a new quotes object with items from [0, index)
def getQuotesSubset(index, symbol, quotes):
    subQuotes = {}
    subQuotes['Symbol']=symbol
    
    subQuotes['Date']=quotes[symbol]['Date'][0:index[symbol]]
    subQuotes['Open']=quotes[symbol]['Open'][0:index[symbol]]
    subQuotes['High']=quotes[symbol]['High'][0:index[symbol]]
    subQuotes['Low']=quotes[symbol]['Low'][0:index[symbol]]
    subQuotes['Close']=quotes[symbol]['Close'][0:index[symbol]]
    subQuotes['Volume']=quotes[symbol]['Volume'][0:index[symbol]]
    subQuotes['AdjClose']=quotes[symbol]['AdjClose'][0:index[symbol]]

    return subQuotes
