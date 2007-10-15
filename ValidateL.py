def PickWindow():
    accuracy=[]
    for window in range(1,242*2,5): # two years
        accuracy.append(ComputeL_Window(window))
        PrintAccuracy(accuracy)
    
def ComputeL_Window(window):   
    print "Processing window " + str(window) + "."
    
    import GetData
    symbols = GetData.GetSymbols()

    win = 0.0
    total = 0

    for symbol in symbols:
        [w, t] = ComputeL_WindowSymbol(window, symbol)
        win = win + w
        total = total + t
    accuracy = win / total

    return [accuracy, total]
    
def ComputeL_WindowSymbol(window, symbol):
    print "Processing window " + str(window) + " and symbol " + symbol + "."
    
    import GetData
    quotes = GetData.GetQuotes(symbol)

    win = 0.0
    total=0
        
    index = 0
    while(index+window+1 < len(quotes)):
        goodDays=0
        for day in range(index, index+window):
            if(float(quotes[day][2])>float(quotes[day][1])*1.02):
                goodDays = goodDays + 1
        L = float(goodDays) / float(window)
        
        # 0.7 is termed the margin.
        # It's conceivable that we should validate to pick it.
        if(L>0.50):
            total = total + 1
            # if high > open * 1.02
            if(float(quotes[index+window+1][2])>float(quotes[index+window+1][1])*1.03):
                win = win + 1
        index = index + 1

    if(total == 0):
        return [0, 0]
    return [win, total]

def PrintAccuracy(accuracy):
    outputFilename = "data/ValidateL.csv"
    outputFile = open(outputFilename, 'w')
    for a in accuracy:
        outputFile.write(str(a[0]) + ", " + str(a[1]) + "\n")
    outputFile.close()

PickWindow()
