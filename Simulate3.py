window = 100
take = 1.02

def Run():
    import GetData
    symbols = GetData.GetSymbols()
    q = GetData.GetAllQuotes()

    import Predictors

    capital = 25000.0
    shares = 0
    
    wins = 0
    total = 0
    loss = 1.0
    loss_total = 0
    
    # now let's simulate
    for day in range(len(q["TIBX"])-2, len(q["TIBX"])-1):

        # remove symbols no longer listed
        for symbol in symbols:
            if(day>=len(q[symbol])):
               symbols.remove(symbol);
        print len(symbols)
               
        L={}
        for symbol in symbols:
            quotes = q[symbol]
            L[symbol] = Predictors.ComputeL(quotes, day, window, take)
        maxL = Predictors.DictionaryMaxN(L, 20)

        K={}
        for symbol in maxL:
            quotes = q[symbol]
            K[symbol] = Predictors.ComputeK(quotes, day, window, take)
        maxK = Predictors.DictionaryMaxN(K, 10)

        J={}
        for symbol in maxK:
            quotes = q[symbol]
            J[symbol] = Predictors.ComputeDayChange(quotes, day)
        symbol = Predictors.DictionaryMin(J)
        quotes = q[symbol]

        Open = float(quotes[day][1])
        High = float(quotes[day][2])
        Close = float(quotes[day][4])
        
        shares = capital / Open
        if(High > Open * take):
            wins = wins + 1
            capital = shares * Open * take
        else:
            capital = shares * Close
            loss = loss * Close/Open
            loss_total = loss_total + 1
        total = total + 1

        import math
        l=loss;
        if(loss_total !=0):
            l = math.pow(loss, 1.0/loss_total)

        print "d: " + str(day) + " s: " + symbol + " c: " + str(capital) + " a: " + str(float(wins)/float(total)) + " loss: " + str(l) + " L: " + str(L[symbol]) + " K: " + str(K[symbol]) + " J: " + str(J[symbol]) 

Run()

