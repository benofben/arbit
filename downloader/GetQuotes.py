import httplib

def getHistoricData(symbol):
    print "Downloading historical data for " + symbol + "..."
    conn = httplib.HTTPConnection("ichart.finance.yahoo.com")

    """
    Notes on the yahoo parameters:
    d=end month-1 (5 = June)
    e=end day
    f=end year
    g=d?
    a=start month-1 (0 = January)
    b=start day
    c=start year
    """ 
    conn.request("GET", "/table.csv?s=" + symbol + "&d=5&e=17&f=2007&g=d&a=0&b=1&c=2002&ignore=.csvc")
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    conn.close()
    if response.status==200 and response.reason=='OK':
        filename = "data/quotes/" + symbol + ".csv"
        file = open (filename, 'w')
        file.write(data)
        file.close()
        print "Saved historical data to " + filename + ".\n"
    else:
        print "Download failed for symbol " + symbol + ".\n"
        return False
    return True

import os
def processSymbolFile():
    if not os.path.exists("data/quotes/"):
        os.makedirs("data/quotes/")
    symbolFilename = "data/symbols/symbols.txt"
    symbolFile = open(symbolFilename, 'r')
    symbols = symbolFile.readlines()
    symbolFile.close()

    failedSymbolsFilename = "data/symbols/failedSymbols.txt"
    failedSymbolsFile = open(failedSymbolsFilename, 'w')
    
    successfulSymbolsFilename = "data/symbols/successfulSymbols.txt"
    successfulSymbolsFile = open(successfulSymbolsFilename, 'w')

    while symbols:
        print str(len(symbols)) + " symbols remaining."
        symbol = symbols.pop()
        symbol = symbol.replace('\n','')
        if not getHistoricData(symbol):
            failedSymbolsFile.write(symbol + '\n')
        else:
            successfulSymbolsFile.write(symbol + '\n')
    successfulSymbolsFile.close()
    failedSymbolsFile.close()

