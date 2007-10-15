window = 100

def Run():
    import GetData
    symbols = GetData.GetSymbols()
    q = GetData.GetAllQuotes()

    import Predictors

    capital = 25000.0
    shares = 0
    
    # now let's simulate
    for day in range(window, len(q["TIBX"])-1):

        L={}
        T={}
        for symbol in symbols:
            quotes = q[symbol]
            [take, expectedReturn] = Predictors.PickTake(quotes, day, window)
            L[symbol] = expectedReturn
            T[symbol] = take
        symbol = Predictors.DictionaryMax(L)

        Open = float(quotes[day][1])
        High = float(quotes[day][2])
        Close = float(quotes[day][4])
        
        shares = capital / Open
        if(High > Open * T[symbol]):
            capital = shares * Open * T[symbol]
        else:
            capital = shares * Close

        print "d: " + str(day) + " s: " + symbol + " c: " + str(capital) + " L: " + str(L[symbol]) + " take: " + str(T[symbol])

Run()
