def run():
    capital=25000
    
    import data
    symbols=data.getSymbols()
    quotes=data.getAllQuotes()

    import datetime
    startDate=datetime.date(2003,1,1)
    endDate=datetime.date.today()

    import os
    if os.path.exists('data/simulate.csv'):
        os.remove('data/simulate.csv')

    # now we simulate for each day
    for day in range(0, (endDate-startDate).days):

        index={}
        for symbol in symbols:
            i=data.getIndex(startDate+datetime.timedelta(days=day), quotes[symbol])
            if i:
                if quotes[symbol]['Volume'][i-1]>500000:
                    index[symbol]=i

        # validate to pick window and take
        A={}
        bestSymbol=""
        for symbol in index:

            import validators
            A[symbol]=validators.FindWindow(quotes[symbol], index[symbol])

            if not bestSymbol:
                bestSymbol=symbol

            if A[symbol]["return"]>A[bestSymbol]["return"]:
                bestSymbol=symbol

        # try the predictor on the current day
        if bestSymbol:
            actualReturn = 0
            Open=quotes[bestSymbol]["Open"][index[bestSymbol]]
            High=quotes[bestSymbol]["High"][index[bestSymbol]]
            Close=quotes[bestSymbol]["Close"][index[bestSymbol]]
            if High>=Open*A[bestSymbol]["take"]:
                capital=capital*A[bestSymbol]["take"]
                actualReturn = A[bestSymbol]["take"]
            else:
                capital=capital*Close/Open
                actualReturn = Close/Open

            s = bestSymbol + '\t' + \
            str(quotes[bestSymbol]["Date"][index[bestSymbol]]) + '\t' + \
            str(round(actualReturn,5)) + '\t' + \
            str(round(A[bestSymbol]["return"],5)) + '\t' + \
            str(A[bestSymbol]["take"]) + '\t' + \
            str(A[bestSymbol]["window"]) + '\t' + \
            str(round(capital,2))
            
            print s

            s = s.replace('\t',',')
            f = open('data/simulate.csv', 'a')
            f.write(s + '\n')
            f.close()

run()
