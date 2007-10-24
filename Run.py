window = 100
take = 1.02

def run():
    import symbols
    symbols.downloadSymbols()

    import quotes
    quotes.downloadAllQuotes()
    
    import data
    symbols = data.getSymbols()
    quotes = data.getAllQuotes()
    
    import predictors

    L={}
    for symbol in symbols:
        index = len(quotes[symbol]["Open"])-1
        if(index and index-window>=0):
            L[symbol] = predictors.L(quotes[symbol], index, window, take)
    maxL = predictors.DictionaryMaxN(L,20)

    K={}
    for symbol in maxL:
        index = len(quotes[symbol]["Open"])-1
        if(index and index-window>0):
            K[symbol] = predictors.K(quotes[symbol], index, window, take)
    maxK = predictors.DictionaryMaxN(K, 10)

    J={}
    for symbol in maxK:
        index = len(quotes[symbol]["Open"])-1
        if(index and index>0):
            J[symbol] = predictors.DailyChange(quotes[symbol], index)
    minJ = predictors.DictionaryMinN(J, 5)
    
    for symbol in minJ:
        index = len(quotes[symbol]["Open"])-1
        print str(quotes[symbol]["Date"][index]) + " s: " + symbol + " L: " + str(L[symbol]) + " K: " + str(K[symbol]) + " J: " + str(J[symbol])

run()
