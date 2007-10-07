window = 100
margin = 0.6
take = 1.02

def Run():
    import downloader.Downloader
#    downloader.Downloader.download()

    import GetData
    symbols = GetData.GetSymbols()
    q = GetData.GetAllQuotes()

    import Predictors
    import time
    L={}
    T={}
    for symbol in symbols:
        day = len(q[symbol])
        l = Predictors.ComputeL(q[symbol], day, window, take)
        if l>margin:
            L[symbol] = l
            T[symbol] = time.localtime(float(q[symbol][day-1][0]))

    for symbol in L:
        timeStr = time.strftime("%a, %d %b %Y", T[symbol])
        print symbol + "," + str(L[symbol]) + "," + timeStr

Run()
