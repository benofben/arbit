import csv
import time
import operator
def ReformatQuoteFile(symbol):
    inputFilename = "data/quotes/" + symbol + ".csv"
    inputFile = open(inputFilename, "rb")
    reader = csv.reader(inputFile)

    quotes=[]
    for Date, Open, High, Low, Close, Volume, AdjClose in reader:
        if Date != "Date":
            timeTuple = time.strptime(Date, "%Y-%m-%d")
            secondsSince1970 = time.mktime(timeTuple)
            quotes.append([secondsSince1970, Open, High, Low, Close, Volume, AdjClose])
    inputFile.close()

    #if the IPO was later than TIBX
    if(quotes[len(quotes)-1][0]>1009947600.0):
        print "Symbol failed because IPO was too recent."
        return False

    quotes=sorted(quotes, key=operator.itemgetter(0))

    if not os.path.exists("data/reformattedQuotes/"):
        os.makedirs("data/reformattedQuotes/")
        
    outputFilename = "data/reformattedQuotes/" + symbol + ".csv"
    outputFile = open(outputFilename, 'w')
    for Date, Open, High, Low, Close, Volume, AdjClose in quotes:
        outputFile.write(str(Date) + "," + Open + "," + High + "," + Low + "," + Close + "," + Volume + "," + AdjClose + "\n")
    outputFile.close()
    return True

import os
def GetSymbols(dirname):
    symbols=[]
    files=os.listdir(dirname)
    for file in files:
        symbols.append(file.replace('.csv',''))
    return symbols

def ReformatQuoteFiles():
    symbolsFilename = "data/symbols/successfullyReformattedSymbols.txt"
    symbolsFile = open(symbolsFilename, 'w')
    
    symbols=GetSymbols('data/quotes')
    while symbols:
        symbol=symbols.pop()
        print "Reformatting symbol " + symbol + "."
        print str(len(symbols)) + " remaining."
        if ReformatQuoteFile(symbol):
            symbolsFile.write(symbol + '\n')
        print " "
        
    symbolsFile.close()
