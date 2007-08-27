import csv
def CreateTrainingSetForWekaForSymbol(stats, train, test, isFirstSymbol):
    inputFilename = "data/train/" + stats['symbol'] + ".csv"
    inputFile = open(inputFilename, "rb")
    
    reader = csv.reader(inputFile)

    # q holds all the quotes for a symbol
    q={}
    q['Date']=[]
    q['Open']=[]
    q['High']=[]
    q['Low']=[]
    q['Close']=[]
    q['Volume']=[]
    q['AdjClose']=[]
    
    for Date, Open, High, Low, Close, Volume, AdjClose in reader:
        q['Date'].append(float(Date))
        q['Open'].append(float(Open))
        q['High'].append(float(High))
        q['Low'].append(float(Low))
        q['Close'].append(float(Close))
        q['Volume'].append(float(Volume))
        q['AdjClose'].append(float(AdjClose))

    window=4

    # copy some symbol-wide statistics that were passed in
    a={}
    for key, value in stats.iteritems():
        a[key]=stats[key]

    # compute average price and volume
    pAvg = 0
    vAvg = 0
    total = 1
    for i in range(window,len(q['Open'])/2):
        pAvg = pAvg + q['Open'][i]
        vAvg = vAvg + q['Volume'][i]
        total = total + 1
    pAvg = pAvg / total
    vAvg = vAvg / total

    a['pGoodDay']=0
    for i in range(window,len(q['Open'])/2):
        a['pGoodDay']=a['pGoodDay']+((q['High'][i]-q['Open'][i])/q['Open'][i])
#    a['pGoodDay']=a['pGoodDay']/(len(q['Open'])/2)
            
    for i in range(window,len(q['Open'])):
        a['l1'] = (q['High'][i-1]-q['Open'][i-1])/q['Open'][i-1]
        a['dailyReturn1'] = (q['Close'][i-1]-q['Close'][i-2])/q['Close'][i-2]
        a['tradingDayReturn1'] = (q['Open'][i-1]-q['Close'][i-1])/q['Open'][i-1]
        
        if(q['High'][i]>q['Open'][i]*1.02):
            a['label']='Good'
        elif(q['Close'][i]>q['Open'][i]):
            a['label']='OK'
        elif(q['Close'][i]>q['Open'][i]*0.98):
            a['label']='Bad'
        else:
            a['label']='Very Bad'

        # Build the header string
        if i==window:
            if isFirstSymbol==1:
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

        # only print some outStrings
        # if(a['l1']>0.08 or a['dailyReturn1']<-0.06 or a['tradingDayReturn1']>0.08):
        # if(a['l1']>0.08 or a['tradingDayReturn1']>0.08):
        # if(a['beta']>2.5):
        if i<len(q['Open'])/2:
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

    train=open("data/weka/train" + ".csv", 'w')
    test=open("data/weka/test" + ".csv", 'w')

#    if os.path.exists("data/weka"):
#        shutil.rmtree("data/weka")
#    os.mkdir("data/weka")

    symbols=downloader.ReformatQuotes.GetSymbols('data/train')
    isFirstSymbol = 1
    while symbols:
        symbol = symbols.pop()
        print "Making weka file for " + symbol + ". " + str(len(symbols)) + " remaining."

        stats={}
        stats['symbol']=symbol
        stats['beta']=float(beta[symbol])
        # stats['marketValue']=float(marketValue[symbol])

        CreateTrainingSetForWekaForSymbol(stats, train, test, isFirstSymbol)
        isFirstSymbol = 0
        
    train.close()
    test.close()
        
def CreateTrainingSetForWeka2(symbol):
    beta = LoadPredictor("beta.csv")
    marketValue = LoadPredictor("marketValue.csv")

    train=open("data/weka/train" + symbol + ".csv", 'w')
    test=open("data/weka/test" + symbol + ".csv", 'w')

    print "Making weka file for " + symbol + ".\n"
    CreateTrainingSetForWekaForSymbol(symbol, beta[symbol], marketValue[symbol], train, test)

    train.close()
    test.close()
