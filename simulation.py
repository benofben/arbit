import data
symbols=data.getSymbols()
quotes=data.getAllQuotes()

import datetime
startDate=datetime.date(2007,1,1)
endDate=datetime.date.today()

import cPickle
def simulation():
    capital=25000
    
    # now we simulate for each day
    for day in range(0, (endDate-startDate).days+1):

        print 'Simulating day ' + str(startDate+datetime.timedelta(days=day)) + '.'

        index={}
        for symbol in symbols:
            i=data.getIndex(startDate+datetime.timedelta(days=day), quotes[symbol])
            if i:
                index[symbol]=i

        responses=[]
        for symbol in index:
            try:
                f=open('data/queue/response/' + str(quotes[symbol]['Date'][index[symbol]-1]) + symbol, 'r')
                response=cPickle.load(f)
                f.close()

                if(len(responses)<1):
                    responses.append(response)
                elif(responses[-1]['Return']<response['Return']):
                    responses[-1]=response
                responses=sorted(responses, lambda x, y: cmp(x['Return'], y['Return']),reverse=True)
            except IOError:
                pass

        if responses:
            rank=0
            bestSymbol=responses[rank]['Symbol']
            
            # try the predictor on the current day
            actualReturn=0
            Open=quotes[bestSymbol]['Open'][index[bestSymbol]]
            High=quotes[bestSymbol]['High'][index[bestSymbol]]
            Close=quotes[bestSymbol]['Close'][index[bestSymbol]]
            if High>=Open*responses[rank]['Take']:
                capital=capital*responses[rank]['Take']
                actualReturn=responses[rank]['Take']
            else:
                capital=capital*Close/Open
                actualReturn=Close/Open
            print str(actualReturn) + '\t' + str(capital)

            f=open('data/simulation.csv','a')
            f.write(str(quotes[bestSymbol]['Date'][index[bestSymbol]]) + ',' + \
                    str(capital) + ',' + \
                    bestSymbol + ',' + \
                    str(rank) + ',' + \
                    str(responses[rank]['Window']) + ',' + \
                    str(actualReturn) + ',' + \
                    str(responses[rank]['Take']) + ',' + \
                    str(responses[rank]['Return']) + '\n')
            f.close()

simulation()
