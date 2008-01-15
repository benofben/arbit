###############################################################################
### Find the window that:
###   (1) Predicts well
###   (2) Has a good return
###############################################################################
def FindWindow(quotes, index):
    bestWindow=1
    bestReturn=1.0
    for window in range(1, 5, 1):
        r = FindReturnForWindow(quotes, index, window)
        
        if r>bestReturn:
            bestReturn=r
            bestWindow=window

    A={}
    A["return"]=bestReturn
    A["window"]=bestWindow
    A["take"]=FindTakeForWindow(quotes, index, bestWindow)
    return A

###############################################################################
### Check how well a particular window predicts
###############################################################################
def FindReturnForWindow(quotes,index,window):
    r=1.0
    total=0
    for d in range(index-window-5,index):
        take=FindTakeForWindow(quotes,d,window)
        Open=quotes["Open"][d]
        High=quotes["High"][d]
        Close=quotes["Close"][d]
        if(High>=Open*take):
            r=r*take
        else:
            r=r*Close/Open
        total=total+1

    import math
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
        for d in range(index-window, index):
            Open=quotes["Open"][d]
            High=quotes["High"][d]
            Close=quotes["Close"][d]
            if(High>=Open*take):
                r=r*take
            else:
                r=r*Close/Open
            total=total+1

        import math
        r=math.pow(r, 1.0/total)
        
        if r>bestReturn:
            bestReturn=r
            bestTake=take

    return bestTake
