import httplib
import csv

# Q = NASDAQ, 1 = AMEX, N = NYSE
exchangeList = ["Q", "1", "N"]

# Dictionary holds a bunch of Symbol and MarketValue
SymbolDictionary={}

def getSymbolLists(exchange):    
    print "Trying to get exchange " + exchange + "..."
    conn = httplib.HTTPConnection("www.nasdaq.com")
    conn.request("GET", "/asp/symbols.asp?exchange=" + exchange + "&start=0")
    response = conn.getresponse()
    
    print response.status, response.reason
    data=response.read()
    conn.close()

    print "Done downloading.  Writing to file.\n"
    file = open("data/symbols/" + exchange + ".csv", "w")
    file.write(data)
    file.close()

# delete the first, second and last lines from a symbols file
def deleteLines(filename):
    inputFile = open(filename, "r")
    all_lines = inputFile.readlines()
    inputFile.close()
    outputFile = open(filename, "w")
    for line in all_lines[2:-1]:
        outputFile.write(line)
    outputFile.close()

def cleanUpMarketValue(MarketValue):
    MarketValue=MarketValue.replace('$','')
    MarketValue=MarketValue.replace(',','')
    return MarketValue

def writeSymbolToDictionary(Symbol, MarketValue):
    if MarketValue != "N/A":
        MarketValue=cleanUpMarketValue(MarketValue)
        Symbol = Symbol.replace('^','.')
        SymbolDictionary[Symbol]=MarketValue
    
def getSymbolList(exchange):
    filename = "data/symbols/" + exchange + ".csv"
    inputFile = open(filename, "rb")
    reader = csv.reader(inputFile)

    if exchange == "Q":
        for Name,Symbol,SecurityType,SharesOutstanding,MarketValue,Description in reader:
            writeSymbolToDictionary(Symbol, MarketValue)
    elif exchange == "1" or exchange == "N":
        for Name,Symbol,MarketValue,Description in reader:
            writeSymbolToDictionary(Symbol, MarketValue)

    inputFile.close()

def printMarketValues(SymbolDictionary):
    filename="data/marketValue.csv"
    outputFile = open(filename, "w")
    for Symbol in SymbolDictionary.keys():
        outputFile.write(Symbol + "," + SymbolDictionary[Symbol] + "\n")
    outputFile.close()


import os
def getSymbols():
    if not os.path.exists("data/symbols/"):
        os.makedirs("data/symbols/")
    for exchange in exchangeList:
        getSymbolLists(exchange)
        deleteLines("data/symbols/" + exchange + ".csv")
        getSymbolList(exchange)
    filename="data/symbols/symbols.txt"
    file = open(filename, "w")
    i=0
    for Symbol in SymbolDictionary.keys():
        # if MarketValue>$1 billion
        if float(SymbolDictionary[Symbol])>1000:
            file.write(Symbol + "\n")
            i=i+1
    file.close()

    printMarketValues(SymbolDictionary)
    
    print "Saved " + str(i) + " symbols."    

getSymbols()
