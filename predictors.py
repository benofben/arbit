def RankQuote(quotes, index):
    A = PickAlpha(quotes, index)
    return A

def PickAlpha(quotes, index):
    A={}
    A['Return'] = 0.0

    for a in range(0,100,3):
        alpha = a/100.0
        B=PickTake(alpha, quotes, index)

        if B['Return']>A['Return']:
            A=B
            A['alpha']=alpha
            
    return A

import math
def PickTake(alpha, quotes, index):
    A={}
    A['Take'] = 1.0
    A['Return'] = 1.0
    
    for t in range(0,50):
        take = 1.0 + t/500.0
        r=0.0
        t=0.0
        
        for day in range(index, 0, -1):
            Open = quotes['Open'][day]
            Close = quotes['Close'][day]
            High = quotes['High'][day]
            if High > Close * take:
                x=take
            else:
                x=Close/Open
            w=math.pow(1-alpha, -1*(day-index))
            r=r+x*w
            t=t+w
        r=r/t

        if r>A['Return']:
            A['Take']=take
            A['Return']=r
    
    return A
