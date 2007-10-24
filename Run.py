window = 200
take = 1.02

def run():
    import symbols
    symbols.downloadSymbols()

    import quotes
    quotes.downloadQuotes()

    import data
    quotes = data.getAllQuotes()
    
    import Predictors
    import time
    L={}
    T={}
    for symbol in symbols:
        lastDay = len(q[symbol])
        L[symbol] = Predictors.ComputeL(q[symbol], lastDay, window, take)
        T[symbol] = time.localtime(float(q[symbol][lastDay-1][0]))

    maxL = Predictors.DictionaryMaxN(L, 10)
    for symbol in maxL:
        timeStr = time.strftime("%a, %d %b %Y", T[symbol])
        print symbol + "," + str(L[symbol]) + "," + timeStr
    """

run()
