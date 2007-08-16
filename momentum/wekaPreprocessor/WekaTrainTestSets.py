import csv
def CreateTrainingSetForWekaForSymbol(symbol, beta, marketValue):
    inputFilename = "data/train/" + symbol + ".csv"
    inputFile = open(inputFilename, "rb")

    header='Low0, Low1, Low2, High0, High1, High2, Vol0, Vol1, Vol2, Close, y\n'
    
    train=open("data/weka/train" + symbol + ".csv", 'w')
    train.write(header)

    test=open("data/weka/test" + symbol + ".csv", 'w')
    test.write(header)

    reader = csv.reader(inputFile)

    quotes=[]
    for Date, Open, High, Low, Close, Volume, AdjClose in reader:
        quotes.append([float(Date), float(Open), float(High), float(Low), float(Close), float(Volume), float(AdjClose)])

    for i in range(3,len(quotes)):
        Low0 = quotes[i-3][3]
        Low1 = quotes[i-2][3]
        Low2 = quotes[i-1][3]
        High0 = quotes[i-3][2]
        High1 = quotes[i-2][2]
        High2 = quotes[i-1][2]
        Vol0 = quotes[i-3][5]
        Vol1 = quotes[i-2][5]
        Vol2 = quotes[i-1][5]
        Close = quotes[i-1][4]
        Open = quotes[i][1]
        if(float(quotes[i][2])>float(quotes[i][1])*1.02):
            y='B';
        else:
            y='N';

        outString = str(Low0) + "," + str(Low1) + "," + str(Low2) + "," + str(High0) + "," + str(High1) + "," + str(High2) + "," + str(Vol0) + "," + str(Vol1) + "," + str(Vol2) + "," + str(Close) + "," + str(y) +'\n'

        if i<len(quotes)/2:
            train.write(outString)
        else:
            test.write(outString)
    train.close()
    inputFile.close()

def LoadPredictor(filename):
    inputFilename = "data/symbols/" + filename
    inputFile = open(inputFilename, "rb")
    reader = csv.reader(inputFile)

    dict={}
    for Symbol, Predictor in reader:
        dict[Symbol]=Predictor

    inputFile.close()

    return dict

import downloader.ReformatQuotes
import os
import shutil
def CreateTrainingSetForWeka():
    beta = LoadPredictor("beta.csv")
    marketValue = LoadPredictor("marketValue.csv")

    if os.path.exists("data/weka"):
        shutil.rmtree("data/weka")
    os.mkdir("data/weka")

    symbols=downloader.ReformatQuotes.GetSymbols('data/train')
    while symbols:
        symbol = symbols.pop()
        print "Making weka file for " + symbol + ". " + str(len(symbols)) + " remaining."
        CreateTrainingSetForWekaForSymbol(symbol, beta[symbol], marketValue[symbol])
        
def CreateTrainingSetForWeka(symbol):
    beta = LoadPredictor("beta.csv")
    marketValue = LoadPredictor("marketValue.csv")

    print "Making weka file for " + symbol + ".\n"
    CreateTrainingSetForWekaForSymbol(symbol, beta[symbol], marketValue[symbol])
