import csv
def CreateTrainingSetForWekaForSymbol(symbol, beta, marketValue, train, test):
    inputFilename = "data/train/" + symbol + ".csv"
    inputFile = open(inputFilename, "rb")
    
    reader = csv.reader(inputFile)

    quotes=[]
    for Date, Open, High, Low, Close, Volume, AdjClose in reader:
        quotes.append([float(Date), float(Open), float(High), float(Low), float(Close), float(Volume), float(AdjClose)])

    a={}
    window=4
    
    pAvg = 0
    vAvg = 0
    total = 1
    for i in range(window,len(quotes)):
        pAvg = pAvg + quotes[i][4]
        vAvg = vAvg + quotes[i][5]
        total = total + 1
    pAvg = pAvg / total
    vAvg = vAvg / total
        
    for i in range(window,len(quotes)):
        a['symbol'] = symbol
        a['beta'] = beta
        a['marketValue'] = marketValue
        
        # a['Low0'] = quotes[i][3]
        # a['Low1'] = quotes[i-1][3]/pAvg
        # a['Low2'] = quotes[i-2][3]/pAvg
        # a['Low3'] = quotes[i-3][3]/pAvg

        High0 = quotes[i][2]
        High1 = quotes[i-1][2]
        High2 = quotes[i-2][2]
        High3 = quotes[i-3][2]
        High4 = quotes[i-4][2]
        # a['High0'] = quotes[i][2]
        # a['High1'] = quotes[i-1][2]/pAvg
        # a['High2'] = quotes[i-2][2]/pAvg
        # a['High3'] = quotes[i-3][2]/pAvg

        # a['Vol1'] = quotes[i-1][5]/vAvg
        # a['Vol2'] = quotes[i-2][5]/vAvg
        # a['Vol3'] = quotes[i-3][5]/vAvg

        Close0 = quotes[i][4]
        Close1 = quotes[i-1][4]
        Close2 = quotes[i-2][4]
        Close3 = quotes[i-3][4]
        Close4 = quotes[i-4][4]
        # a['Close0'] = quotes[i][4]
        # a['Close1'] = quotes[i-1][4]/pAvg
        # a['Close2'] = quotes[i-2][4]/pAvg
        # a['Close3'] = quotes[i-3][4]/pAvg
        # a['Close4'] = quotes[i-4][4]/pAvg

        Open0 = quotes[i][1]
        Open1 = quotes[i-1][1]
        Open2 = quotes[i-2][1]
        Open3 = quotes[i-3][1]
        # a['Open0'] = quotes[i][1]
        # a['Open1'] = quotes[i-1][1]/pAvg
        # a['Open2'] = quotes[i-2][1]/pAvg
        # a['Open3'] = quotes[i-3][1]/pAvg
                        
        # a['p1'] = (a['High0']-a['Open0'])/a['Open0']
        # a['p2'] = (a['High0']-a['Close1'])/a['Close1']
        # a['p3'] = (a['Open0']-a['Close1'])/a['Close1']

        a['l1'] = (High1-Open1)/Open1
        # a['l2'] = (High2-Open2)/Open2
        # a['l3'] = (High3-Open3)/Open3

        # a['dailyReturn0'] = (a['Close0']-a['Close1'])/a['Close1']
        a['dailyReturn1'] = (Close1-Close2)/Close2
        # a['dailyReturn2'] = (Close2-Close3)/Close3
        # a['dailyReturn3'] = (Close3-Close4)/Close4

        a['tradingDayReturn1'] = (Open1-Close1)/Open1
        # a['tradingDayReturn2'] = (Open2-Close2)/Open2
        # a['tradingDayReturn3'] = (Open3-Close3)/Open3
        
        if(High0>Open0*1.02):
            a['label']='Good'
        elif(Close0>Open0):
            a['label']='OK'
        elif(Close0>Open0*0.98):
            a['label']='Bad'
        else:
            a['label']='Very Bad'

        # Builder the header string
        if i==window:
            header=''
            for key, value in a.iteritems():
                if(key != 'label'):
                    header=header + key + ','
            header = header + 'label\n'
            train.write(header)
            test.write(header)

        # Build the string containing the data
        outString=''
        for key, value in a.iteritems():
            if(key != 'label'):
                outString = outString + str(value) + ','
        outString = outString + a['label'] + '\n'

        if i<len(quotes)/2:
            train.write(outString)
        else:
            test.write(outString)
            
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

    train=open("data/weka/train" + symbol + ".csv", 'w')
    test=open("data/weka/test" + symbol + ".csv", 'w')

    print "Making weka file for " + symbol + ".\n"
    CreateTrainingSetForWekaForSymbol(symbol, beta[symbol], marketValue[symbol], train, test)

    train.close()
    test.close()
