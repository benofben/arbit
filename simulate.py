window = 100
take = 1.02

def run():
    capital = 25000.0
    
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
                L[symbol] = predictors.L(quotes[symbol], index, window, take)
        maxL = predictors.DictionaryMaxN(L,20)

        K={}
        for symbol in maxL:
            index = data.getIndex(startDate + datetime.timedelta(days=day), quotes[symbol])
            if(index and index-window>0):
                K[symbol] = predictors.NDayLow(quotes[symbol], index)
        maxK = predictors.DictionaryMaxN(K, 10)

        J={}
        for symbol in maxK:
            index = data.getIndex(startDate + datetime.timedelta(days=day), quotes[symbol])
            if(index and index>0):
                J[symbol] = predictors.DailyChange(quotes[symbol], index)
        symbol = predictors.DictionaryMin(J)

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
            print d + " s: " + symbol + " c: " + str(capital) + " a: " + str(float(wins)/float(total)) + " loss: " + str(l) + " L: " + str(L[symbol]) + " K: " + str(K[symbol]) + " J: " + str(J[symbol])

run()

