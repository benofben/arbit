import data
symbols=data.getSymbols()
quotes=data.getAllQuotes()

import datetime
startDate=datetime.date(2007,1,1)
endDate=datetime.date.today()

def simulate():
    import cPickle

    capital=25000
    
    # now we simulate for each day
    for day in range(0, (endDate-startDate).days+1):

        print 'Simulating day ' + str(startDate+datetime.timedelta(days=day)) + '.'

        index={}
        for symbol in symbols:
            i=data.getIndex(startDate+datetime.timedelta(days=day), quotes[symbol])
            if i:
                index[symbol]=i

        # load the responses for today into memory and
        # pick the symbol we are going to buy today
        A={}
        bestSymbol=''
        for symbol in index:
            try:
                f=open('data/queue/response/' + str(startDate+datetime.timedelta(days=day)) + symbol, 'r')
                response=cPickle.load(f)
                A[response['Symbol']]=response
                f.close()

                if not bestSymbol:
                    bestSymbol=symbol
                if A[symbol]['Return']>A[bestSymbol]['Return']:
                    bestSymbol=symbol
                    
            except IOError:
                pass

        # try the predictor on the current day
        if bestSymbol:
            actualReturn=0
            Open=quotes[bestSymbol]['Open'][index[bestSymbol]]
            High=quotes[bestSymbol]['High'][index[bestSymbol]]
            Close=quotes[bestSymbol]['Close'][index[bestSymbol]]
            if High>=Open*A[bestSymbol]['Take']:
                capital=capital*A[bestSymbol]['Take']
                actualReturn=A[bestSymbol]['Take']
            else:
                capital=capital*Close/Open
                actualReturn=Close/Open

            f=open('data/simulation.csv','a')
            f.write(str(quotes[bestSymbol]['Date'][index[bestSymbol]]) + ',' + \
                    str(capital) + ',' + \
                    bestSymbol + ',' + \
                    str(A[bestSymbol]['Window']) + ',' + \
                    str(actualReturn) + ',' + \
                    str(A[bestSymbol]['Take']) + ',' + \
                    str(A[bestSymbol]['Return']) + '\n')
            f.close()

simulate()
