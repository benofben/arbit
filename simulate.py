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

        index={}
        for symbol in symbols:
            i = data.getIndex(startDate + datetime.timedelta(days=day), quotes[symbol])
            if(i and i-100>=0):
                index[symbol] = i

        L={}
        for symbol in index:
            L[symbol] = predictors.L(quotes[symbol], index[symbol], 100, take)
        maxL = predictors.DictionaryMaxN(L, 10)

        K={}
        for symbol in maxL:
            K[symbol] = predictors.L(quotes[symbol], index[symbol], 50, take)
        maxK = predictors.DictionaryMaxN(K, 5)

        J={}
        for symbol in maxK:
            J[symbol] = predictors.DailyChange(quotes[symbol], index[symbol])
        symbol = predictors.DictionaryMax(J)

        if(index):
            average = predictors.AverageL(index, quotes, index, take)
            averageL = predictors.AverageL(maxL, quotes, index, take)
            averageLK = predictors.AverageL(maxK, quotes, index, take)
            print str(average) + " " + str(averageL) + " " + str(averageLK)
            
        if(index):
            Open = quotes[symbol]["Open"][index[symbol]]
            High = quotes[symbol]["High"][index[symbol]]
            Close = quotes[symbol]["Close"][index[symbol]]

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
            print d + " s: " + symbol + " c: " + str(capital) + " a: " + str(float(wins)/float(total)) + " loss: " + str(l) + " L: " + str(L[symbol])+ " K: " + str(K[symbol]) + " J: " + str(J[symbol])

run()

