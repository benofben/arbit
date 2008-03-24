import datetime
import data
import math
startDate=datetime.date(2007,1,1)
endDate=datetime.date(2007,3,1)

def main():
    symbols=data.getSymbols()
    quotes=data.getAllQuotes()

    file = open('data/alphaPlot.csv', 'w')
    fileTotal = open('data/alphaPlotTotals.csv', 'w')
    
    for a in range(0,30,1):
        alpha = a/30.0
        print 'alpha: ' + str(alpha)
        [array, total]=simulate(alpha, symbols, quotes)

        for b in range(0,10):
            file.write(str(array[b]) + ',')
            fileTotal.write(str(total[b]) + ',')
        file.write('\n')
        fileTotal.write('\n')
    file.close()
    fileTotal.close()
        
def pwin(quotes, index):
    Open = quotes['Close'][index-1]
    Close = quotes['Close'][index]
    High = quotes['High'][index]
    if High > Open * 1.02:
        return 1.0
    else:
        return 0.0
    
def simulate(alpha, symbols, quotes):
    total=0.0
    emaSum=0.0
    pwinSum=0.0

    array={}
    total={}
    for b in range(0,10):
        array[b]=0.0
        total[b]=0.0
        
    for day in range(0, (endDate-startDate).days):
        currentDate=startDate+datetime.timedelta(days=day)

        index={}
        for symbol in symbols:
            i=data.getIndex(currentDate, quotes[symbol])
            if i:
                if quotes[symbol]['Volume'][i-1]>500000:
                    index[symbol]=i

        for symbol in index:
            e=computeMinMaxPredictor(quotes[symbol], index[symbol]-1, alpha)    
            pw=pwin(quotes[symbol], index[symbol])

            for b in range(0,10):
                bin = b/500.0
                if(e>bin):
                    array[b]=array[b]+pw
                    total[b]=total[b]+1

    for b in range(0,10):
        if total[b]>0:
            array[b]=array[b]/total[b]
    return [array, total]
        
def computeExpectedReturn(quotes, index, alpha, take):
    r=0.0
    t=0.0
    for day in range(index, 0, -1):
        Open = quotes['Open'][day]
        Close = quotes['Close'][day]
        High = quotes['High'][day]
        if High > Open * take:
            x=take
        else:
            x=Close/Open
        w=math.pow(1-alpha, -1*(day-index))
        r=r+x*w
        t=t+w
    r=r/t
    return r

def computeMinMaxPredictor(quotes, index, alpha):
    r=0.0
    t=0.0
    for day in range(index, 0, -1):
        Open = quotes['Open'][day]
        Close = quotes['Close'][day]
        High = quotes['High'][day]
        Low = quotes['Low'][day]

        u=(High-max(Open, Close))/max(Open, Close)
        d=(min(Open, Close)-Low)/min(Open, Close)
        x=u
            
        w=math.pow(1-alpha, -1*(day-index))
        r=r+x*w
        t=t+w
    
    if t==0:
        return 0
    return r/t

main()
