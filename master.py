import sys
import cPickle
import stomp
 
class MyListener(object):
    i=0
    
    def on_error(self, headers, message):
        print 'received an error %s' % message
        
    def on_message(self, headers, message):
        print 'got a message' + str(i)
    
def run():
    conn = stomp.Connection()
    conn.start()
    conn.connect()

    capital=25000
    
    import data
    symbols=data.getSymbols()
    quotes=data.getAllQuotes()

    import datetime
    startDate=datetime.date(2003,1,2)
    endDate=datetime.date.today()

    # now we simulate for each day
    for day in range(0, (endDate-startDate).days):

        index={}
        for symbol in symbols:
            i=data.getIndex(startDate+datetime.timedelta(days=day), quotes[symbol])
            if i:
                index[symbol]=i

        # publish a computation request JMS message for each symbol
        for symbol in index:
            print "Publishing " + symbol + " for " + str(startDate+datetime.timedelta(days=day))
            subQuotes=data.getQuotesSubset(index, symbol, quotes)
            conn.send(cPickle.dumps(subQuotes), destination='/queue/request')

    conn.disconnect()
    
    '''
        # now wait for the results to come back from the JMS server
        while(len(responses)<len(index)):
            response=receive()
            responses[response['Symbol']]=response
            print "Received response " + len(responses) + " of " + len(index)

        # pick the symbol we are going to buy today
        bestSymbol=''
        for symbol in index:            
            if not bestSymbol:
                bestSymbol=symbol
            if A[symbol]['Return']>A[bestSymbol]['Return']:
                bestSymbol=symbol

        # try the predictor on the current day
        if bestSymbol:
            Open=quotes[bestSymbol]['Open'][index[bestSymbol]]
            High=quotes[bestSymbol]['High'][index[bestSymbol]]
            Close=quotes[bestSymbol]['Close'][index[bestSymbol]]
            if High>=Open*A[bestSymbol]['Take']:
                capital=capital*A[bestSymbol]['Take']
            else:
                capital=capital*Close/Open

            print 'Symbol: ' + bestSymbol + \
            ' Expected Return: ' + str(A[bestSymbol]['Return']) + \
            ' Window: ' + str(A[bestSymbol]['Window']) + \
            ' Take: ' + str(A[bestSymbol]['Take'])

            print str(quotes[bestSymbol]['Date'][index[bestSymbol]]) + \
            ' C: ' + str(capital) + ' Now: ' + str(datetime.datetime.now())
    '''

run()

