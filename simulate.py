def run():
    capital=25000
    
    import data
    symbols=data.getSymbols()
    quotes=data.getAllQuotes()

    import datetime
    startDate=datetime.date(2007,10,1)
    endDate=datetime.date(2008,1,1)

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
        bestSymbol=''
        for symbol in index:

            import predictors
            A[symbol]=predictors.RankQuote(quotes[symbol], index[symbol])

            if not bestSymbol:
                bestSymbol=symbol

            if A[symbol]['Return']>A[bestSymbol]['Return']:
                bestSymbol=symbol

        # try the predictor on the current day
        if bestSymbol:
            actualReturn = 0
            Open=quotes[bestSymbol]['Open'][index[bestSymbol]]
            High=quotes[bestSymbol]['High'][index[bestSymbol]]
            Close=quotes[bestSymbol]['Close'][index[bestSymbol]]
            if High>=Open*A[bestSymbol]['Take']:
                capital=capital*A[bestSymbol]['Take']
                actualReturn = A[bestSymbol]['Take']
            else:
                capital=capital*Close/Open
                actualReturn = Close/Open

            s = bestSymbol + '\t' + \
            str(quotes[bestSymbol]['Date'][index[bestSymbol]]) + '\t' + \
            str(round(actualReturn,5)) + '\t' + \
            str(round(A[bestSymbol]['Take'],5)) + '\t' + \
            str(round(A[bestSymbol]['Return'],5)) + '\t' + \
            str(round(A[bestSymbol]['alpha'],5)) + '\t' + \
            str(round(capital,2))
            print s

            s = s.replace('\t',',')
            f = open('data/simulate.csv', 'a')
            f.write(s + '\n')
            f.close()

run()
