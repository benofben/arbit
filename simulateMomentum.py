window = 100
take = 1.02

def run():
    #import symbols
    #symbols.downloadSymbols()

    #import quotes
    #quotes.downloadAllQuotes()
    
    # clear the old file
    outputFilename = "data/momentumSimulate.csv"
    outputFile = open(outputFilename, 'w')
    outputFile.close()
    
    capital = 25000.0
    shares = 0
    
    wins = 0
    total = 0
    loss = 1.0
    loss_total = 0

    import data
    symbols = data.getSymbols()
    quotes = data.getAllQuotes()

    import datetime
    startDate = datetime.date(2003,1,1)
    endDate = datetime.date.today()
    
    import predictors
          
    # now let's simulate
    for day in range(0, (endDate-startDate).days):
        L={}
        for symbol in symbols:
            index = data.getIndex(startDate + datetime.timedelta(days=day), quotes[symbol])
            if(index and index-window>=0):
                L[symbol] = predictors.NDayLow(quotes[symbol],index)
        maxL = predictors.DictionaryMaxN(L,5)

        K={}
        for symbol in symbols:
            index = data.getIndex(startDate + datetime.timedelta(days=day), quotes[symbol])
            if(index and index-window>0):
                K[symbol] = predictors.DailyChange(quotes[symbol], index)
        symbol = predictors.DictionaryMin(K)

        if(symbol):
            index = data.getIndex(startDate + datetime.timedelta(days=day), quotes[symbol])
        if(symbol and index):
            Open = quotes[symbol]["Open"][index]
            High = quotes[symbol]["High"][index]
            Close = quotes[symbol]["Close"][index]

            if(High > Open * take):
                wins = wins + 1
                capital = capital * take
            else:
                shares = capital / Open
                capital = shares * Close
            
                loss = loss * Close/Open
                loss_total = loss_total + 1
                
            total = total + 1

            import math
            l=loss;
            if(loss_total !=0):
                l = math.pow(loss, 1.0/loss_total)

            d = (startDate + datetime.timedelta(days=day)).isoformat()
            print d + " s: " + symbol + " c: " + str(capital) + " a: " + str(float(wins)/float(total)) + " loss: " + str(l) + " L: " + str(L[symbol]) + " K: " + str(K[symbol])

            outputFilename = "data/momentumSimulate.csv"
            outputFile = open(outputFilename, 'a')
            outputFile.write(str(day) + "," + str(capital) + "," + str(float(wins)/float(total)) + "," + str(l) + "," + str(L[symbol]) + "," + str(K[symbol]) + "\n")
            outputFile.close()

run()
