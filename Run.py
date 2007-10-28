window = 100

def run():
    #import symbols
    #symbols.downloadSymbols()

    #import quotes
    #quotes.downloadAllQuotes()
    
    import data
    symbols = data.getSymbols()
    quotes = data.getAllQuotes()
    
    import predictors

    L={}
    for symbol in symbols:
        index = len(quotes[symbol]["Open"])-1
        nDayHigh = predictors.NDayHigh(quotes[symbol],index)
        if(nDayHigh>=300):
            L[symbol] = nDayHigh

    K={}
    for symbol in L:
        index = len(quotes[symbol]["Open"])-1
        K[symbol] = predictors.DailyChange(quotes[symbol], index)
    KMax = predictors.DictionaryMaxN(K, 5)
    
    for symbol in KMax:
        index = len(quotes[symbol]["Open"])-1
        print str(quotes[symbol]["Date"][index]) + " s: " + symbol + " L: " + str(L[symbol]) + " K: " + str(K[symbol])

run()
