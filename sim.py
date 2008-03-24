import datetime
import data
import math
startDate=datetime.date(2007,1,1)
endDate=datetime.date(2007,3,1)

def main():
    symbols=data.getSymbols()
    quotes=data.getAllQuotes()

    take=1.02
    for a in range(0,10,1):
        alpha = a/100.0
        r=simulate(alpha, take, symbols, quotes)
        print str(take) + '\t' + str(alpha) + '\t' + str(r)
    
def simulate(alpha, take, symbols, quotes):
    r=1.0
    
    for day in range(0, (endDate-startDate).days):
        currentDate=startDate+datetime.timedelta(days=day)
        [bestSymbol, bestReturn, bestR2]=testHypothesis(alpha, take, symbols, quotes, currentDate)

        if bestSymbol:
            i=data.getIndex(currentDate, quotes[bestSymbol])
            Open=quotes[bestSymbol]['Open'][day]
            Close = quotes[bestSymbol]['Close'][day]
            High = quotes[bestSymbol]['High'][day]

            if High > Open * take:
                r=r*take
            else:
                r=r*(Close/Open)
        r=math.pow(r, 1.0/(endDate-startDate).days)
    
    return r

def testHypothesis(alpha, take, symbols, quotes, currentDate):
    index={}
    for symbol in symbols:
        i=data.getIndex(currentDate, quotes[symbol])
        if i:
            if quotes[symbol]['Volume'][i-1]>500000:
                index[symbol]=i

    bestReturn=0
    bestSymbol=''
    bestR2=0
    
    for symbol in index:    
        r=computeExpectedReturn(alpha, take, quotes[symbol], index[symbol])
        r2=computeMinMaxPredictor(alpha, take, quotes[symbol], index[symbol])
        
        if not bestSymbol:
            bestSymbol=symbol

        if r>bestReturn:
            bestSymbol=symbol
            bestReturn=r
            bestR2=r2
            
    return [bestSymbol, bestReturn, bestR2]
        
def computeExpectedReturn(alpha, take, quotes, index):
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

def computeMinMaxPredictor(alpha, take, quotes, index):
    r=0.0
    t=0.0
    for day in range(index, 0, -1):
        Open = quotes['Open'][day]
        Close = quotes['Close'][day]
        High = quotes['High'][day]
        Low = quotes['Low'][day]

        u=High-max(Open, Close)
        d=min(Open, Close)-Low
        x=u+d
            
        w=math.pow(1-alpha, -1*(day-index))
        r=r+x*w
        t=t+w
    r=r/t
    return r

main()
