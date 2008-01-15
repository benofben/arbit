import math

###############################################################################
### For the given quotes, find the window that
###   (1) Predicts well
###   (2) Has a good return
### Also find the return and take.
###############################################################################
def EvaluateQuotes(quotes):
    bestWindow=1
    bestReturn=1.0

    for window in range(10, 100, 5):
        r = FindReturnForWindow(quotes, window)
        
        if r>bestReturn:
            bestReturn=r
            bestWindow=window

    A={}
    A['Return']=bestReturn
    A['Window']=bestWindow
    A['Take']=FindTakeForWindow(quotes, len(quotes['Open']), bestWindow)
    return A

###############################################################################
### Test how well a particular window predicts
###############################################################################
def FindReturnForWindow(quotes, window):
    r=1.0
    total=0
    for day in range(window, len(quotes['Open'])):
        take=FindTakeForWindow(quotes, day, window)
        Open=quotes['Open'][day]
        High=quotes['High'][day]
        Close=quotes['Close'][day]
        if(High>=Open*take):
            r=r*take
        else:
            r=r*Close/Open
        total=total+1

    if total:
        r=math.pow(r, 1.0/total)
    
    return r

###############################################################################
### Find the best take for a particular window from [index-window,index)
###############################################################################
def FindTakeForWindow(quotes, index, window):
    bestReturn=1.0;
    bestTake=1.0;
    for t in range(0, 100, 5):
        take=1+t/1000.0

        r=1.0
        total=0
        for day in range(index-window, index):
            Open=quotes['Open'][day]
            High=quotes['High'][day]
            Close=quotes['Close'][day]
            if(High>=Open*take):
                r=r*take
            else:
                r=r*Close/Open
            total=total+1

        r=math.pow(r, 1.0/total)

        if r>bestReturn:
            bestReturn=r
            bestTake=take

    return bestTake
