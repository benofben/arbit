window = 93
margin = 0.7
take = 1.02

def Run():
    import GetData
    symbols = GetData.GetSymbols()
    q = GetData.GetAllQuotes()

    import Predictors
    capital = 25000.0

    # now let's simulate
    for day in range(window, len(q["TIBX"])-1):
        print "Simulating day " + str(day) + "."

        L={}
        for symbol in symbols:
            l = Predictors.ComputeL(q[symbol], day, window, take)
            if l>margin:
                L[symbol] = l

        K={}
        for symbol in L:
            K[symbol] = Predictors.ComputeK(q[symbol], day, 3, take)
            
        symbol = Predictors.DictionaryMin(K)
        quotes = q[symbol]
        Open = float(quotes[day][1])
        High = float(quotes[day][2])
        Close = float(quotes[day][4])
        if(High > Open * take):
            capital = capital * take
        else:
            capital = capital * (Close / Open)
        print str(L[symbol]) + "," + symbol + "," + str(capital) + "," + str(K[symbol])
        
Run()

