# find the window that:
#   (1) Predicts well
#   (2) Has a good return
def FindWindow(quotes, index, maxWindow):
    bestWindow=1
    bestReturn=1
    for window in range(1,maxWindow):
        r = 1.0
        total = 0
        for d in range(index-window, index):
            take=FindTakeForWindow(quotes, d, window)
            Open = quotes["Open"][d]
            High = quotes["High"][d]
            Close = quotes["Close"][d]
            if(High >= Open * take):
                r=r*take
            else:
                r=r*Close/Open
            total = total + 1

        import math
        r = math.pow(r, 1.0/total)

        if(r>bestReturn):
            bestReturn=r
            bestWindow=window

    A={}
    A["return"]=bestReturn
    A["window"]=bestWindow
    A["take"]=FindTakeForWindow(quotes, index, bestWindow)
    return A

def FindTakeForWindow(quotes, index, window):
    bestReturn = 0;
    bestTake = 0;
    for t in range(0,100,5):
        take = 1 + t / 1000.0

        r = 1.0
        total = 0
        # this loop validates over previous days
        for d in range(index-window, index):
            Open = quotes["Open"][d]
            High = quotes["High"][d]
            Close = quotes["Close"][d]
            if(High >= Open * take):
                r=r*take
            else:
                r=r*Close/Open
            total = total + 1

        r = r - 1
        r = r / total
        if(r>bestReturn):
            bestReturn = r
            bestTake = take

    return bestTake

