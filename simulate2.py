maxWindow = 30

def run():
    capital = 25000
    
    import data
    symbols = data.getSymbols()
    quotes = data.getAllQuotes()

    import datetime
    startDate = datetime.date(2003,1,1)
    endDate = datetime.date.today()

    # now we simulate for each day
    for day in range(0, (endDate-startDate).days):

        index={}
        for symbol in symbols:
            i = data.getIndex(startDate + datetime.timedelta(days=day), quotes[symbol])
            if(i and i-maxWindow>=0):
                index[symbol] = i

        # validate to pick window and take
        A={}
        bestSymbol=""
        for symbol in index:

            import validators
            A[symbol]=validators.FindWindow(quotes[symbol], index[symbol], maxWindow)

            if(not bestSymbol):
                bestSymbol = symbol

            if(A[symbol]["return"]>A[bestSymbol]["return"]):
                bestSymbol = symbol

        # try the predictor on the current day
        if(bestSymbol):
            Open = quotes[bestSymbol]["Open"][day]
            High = quotes[bestSymbol]["High"][day]
            Close = quotes[bestSymbol]["Close"][day]
            if(High >= Open * A[bestSymbol]["take"]):
                capital = capital * A[bestSymbol]["take"]
            else:
                capital = capital * Close/Open

            print "Symbol: " + bestSymbol + " Expected Return: " + str(A[bestSymbol]["return"]) + " Window: " + str(A[bestSymbol]["window"]) + " Take: " + str(A[bestSymbol]["take"])
            print str(quotes[bestSymbol]["Date"][index[bestSymbol]]) + " c: " + str(capital)

run()

