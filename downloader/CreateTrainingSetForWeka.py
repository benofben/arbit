
import csv
def CreateTrainingSetForWekaForSymbol(symbol, beta, marketValue,f):
    inputFilename = "data/train/" + symbol + ".csv"
    inputFile = open(inputFilename, "rb")
    reader = csv.reader(inputFile)

    quotes=[]
    for Date, Open, High, Low, Close, Volume, AdjClose in reader:
        quotes.append([Date, Open, High, Low, Close, Volume, AdjClose])

    for i in range(3,len(quotes)):
        Low0 = quotes[i-3][3]
        Low1 = quotes[i-2][3]
        Low2 = quotes[i-1][3]
        High0 = quotes[i-3][2]
        High1 = quotes[i-2][2]
        High2 = quotes[i-1][2]
        Vol0 = quotes[i-1][5]
        Vol1 = quotes[i-1][5]
        Vol2 = quotes[i-1][5]
        Close = quotes[i-1][4]
        if(float(quotes[i][2])>float(quotes[i][1])*1.02):
            y='B';
        else:
            y='N';
        f.write(symbol + "," + beta + "," + marketValue + "," + Low0 + "," + Low1 + "," + Low2 + "," + High0 + "," + High1 + "," + High2 + "," + Vol0 + "," + Vol1 + "," + Vol2 + "," + Close + "," + str(y) +'\n')
        
    inputFile.close()

def LoadPredictor(filename):
    inputFilename = "data/" + filename
    inputFile = open(inputFilename, "rb")
    reader = csv.reader(inputFile)

    dict={}
    for Symbol, Predictor in reader:
        dict[Symbol]=Predictor

    inputFile.close()

    return dict

import ReformatQuotes
def CreateTrainingSetForWeka():
    beta = LoadPredictor("beta.csv")
    marketValue = LoadPredictor("marketValue.csv")

    f=open('data/weka.csv', 'w')
    f.write('Symbol, Beta, MarketValue, Low0, Low1, Low2, High0, High1, High2, Vol0, Vol1, Vol2, Close, y\n')
    symbols=ReformatQuotes.GetSymbols('data/train')
#    while symbols:
#        symbol = symbols.pop()

    for symbol in ['BEAS']:

        #garbarge market value if I can't find one
        if(marketValue.has_key(symbol)):
            mv=marketValue[symbol]
        else:
            mv=str(1000)
                
        CreateTrainingSetForWekaForSymbol(symbol, beta[symbol], mv,f)
    f.close()
    
CreateTrainingSetForWeka()
