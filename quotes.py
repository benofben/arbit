def downloadQuotes(symbol):
    print "Downloading historical data for " + symbol + "..."
    import httplib
    conn = httplib.HTTPConnection("ichart.finance.yahoo.com")

    """
    Notes on the yahoo parameters:
    d=end month-1 
    e=end day
    f=end year
    g=d?
    a=start month-1 (0 = January)
    b=start day (2)
    c=start year (2002)
    """

    import datetime    
    today = datetime.date.today()
    endYear = today.strftime("%Y")
    endMonth = str(int(today.strftime("%m"))-1)
    endDay = today.strftime("%d")
    
    startYear = "2002"
    startMonth = "0"
    startDay = "1"

    conn.request("GET", "/table.csv?s=" + symbol + "&d=" + endMonth + "&e=" + endDay + "&f=" + endYear + "&g=d&a=" + startMonth + "&b=" + startDay + "&c=" + startYear + "&ignore=.csvc")
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    conn.close()
    if response.status==200 and response.reason=='OK':
        reformatAndSaveQuotes(data, symbol)
        print "Saved historical data for " + symbol + ".\n"
    else:
        print "Download failed for symbol " + symbol + ".\n"
        return False
    return True

def reformatAndSaveQuotes(data, symbol):
    quotes=[]
    lines = data.split('\n')
    i=0
    for line in lines:
        if(i>0):
            quotes.append(line)
        i=i+1

    # we want the list to go from oldest quote to newest
    quotes.reverse()

    filename = "data/quotes/" + symbol + ".csv"
    file = open(filename, 'w')
    i=0
    for line in quotes:
        if(i>0):
            file.write(line + "\n")
        i=i+1
    file.close()

def downloadAllQuotes():
    import os
    if os.path.exists("data/quotes"):
        import shutil
        shutil.rmtree("data/quotes")
    os.makedirs("data/quotes/")
    
    symbolFilename = "data/symbols/symbols.txt"
    symbolFile = open(symbolFilename, 'r')
    symbols = symbolFile.readlines()
    symbolFile.close()

    failedSymbolsFilename = "data/symbols/failedSymbols.txt"
    failedSymbolsFile = open(failedSymbolsFilename, 'w')

    while symbols:
        print str(len(symbols)) + " symbols remaining."
        symbol = symbols.pop()
        symbol = symbol.replace('\n','')
        if not downloadQuotes(symbol):
            failedSymbolsFile.write(symbol + '\n')

    failedSymbolsFile.close()

downloadAllQuotes()
