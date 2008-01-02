import cPickle
import httplib
import time
    
def send(quotes):
    pickledQuotes = cPickle.dumps(quotes)
    conn = httplib.HTTPConnection('localhost', 8161)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn.request('POST', '/demo/message/FOO/BAR', 'destination=request&type=queue&body=' + pickledQuotes, headers)
    response = conn.getresponse()
    if response.status!=200 or response.reason!='OK':
        print 'Could not send message to queue.'
        print response.status, response.reason
    
    data = response.read()
    conn.close()

def receive():
    while(True):
        conn = httplib.HTTPConnection('localhost', 8161)
        conn.request('GET', '/demo/message/response?timeout=1000&type=queue')
        response=conn.getresponse()
        data=response.read()
        conn.close()

        if response.status==200 and response.reason=='OK':
            return cPickle.loads(data)
        else:
            print 'Could not get message from queue.  Will try again in 5 seconds.'
            time.sleep(5)
        
def run():
    capital=25000
    
    import data
    symbols=data.getSymbols()
    quotes=data.getAllQuotes()

    import datetime
    startDate=datetime.date(2003,1,1)
    endDate=datetime.date.today()

    # now we simulate for each day
    for day in range(0, (endDate-startDate).days):

        index={}
        for symbol in symbols:
            i=data.getIndex(startDate+datetime.timedelta(days=day), quotes[symbol])
            if i:
                index[symbol]=i

        # resest the responses before we start sending stuff to the server
        responses={}

        # publish a computation request JMS message for each symbol
        for symbol in index:
            subQuotes=data.getQuotesSubset(index, symbol, quotes)
            print "Publishing " + symbol + " for " + str(startDate+datetime.timedelta(days=day))
            send(subQuotes)

        # now wait for the results to come back from the JMS server
        while(len(responses)<len(index)):
            response=receive()
            responses[response['Symbol']]=response
            print "Received response " + len(responses) + " of " + len(index)

        '''
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
