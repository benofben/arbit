def ComputeNDayLow(quotes, day):
    nDayLow = 0;
    Close = float(quotes[day-1][4])

    for d in range(day-2, -1, -1):
        Low = float(quotes[d][3])
        if(Close<=Low):
            nDayLow = nDayLow + 1
        else:
            break
    return nDayLow

def ComputeDayChange(quotes, day):
    TodayClose = float(quotes[day-1][4])
    YesterDayClose = float(quotes[day-2][4])
    return TodayClose / YesterDayClose

def ExpectedReturn(quotes, day, window, take):
    e = 1;
    for d in range(day-window, day):
        Open = float(quotes[d][1])
        High = float(quotes[d][2])
        Close = float(quotes[d][4])
        
        if(High > Open * take):
            e = e * take;
        else:
            e = e * (Close / Open)
    import math
    return math.pow(e, 1.0/window)

def PickTake(quotes, day, window):
    E={}
    for t in range(0,10,1):
        take = 1.0 + float(t)/200
        E[take] = ExpectedReturn(quotes, day, window, take)
    take = DictionaryMax(E)
    return [take, E[take]]

# gain function            
def ComputeL(quotes, day, window, take):
    win = 0.0
    total = 0

    for d in range(day-window, day):
        Open = float(quotes[d][1])
        High = float(quotes[d][2])
        if(High >= Open * take):
            win = win + 1
        total = total + 1

    return win / total

# loss function
def ComputeK(quotes, day, window, take):
    loss = 1.0
    total = 0
    
    for d in range(day-window, day):
        Open = float(quotes[d][1])
        High = float(quotes[d][2])
        Close = float(quotes[d][4])
        if(High < Open * take):
            loss = loss * (Close / Open)
            total = total + 1

    import math
    loss = math.pow (loss, 1.0/total)
    
    return loss

# returns the key of the smallest item in the dictionary
def DictionaryMax(dictionary):
    # pick the first
    m = ""
    for item in dictionary:
        m = item
        break
    # find the max
    for item in dictionary:
        if dictionary[item] > dictionary[m]:
            m = item
    return m

# returns the key of the largest item in the dictionary
def DictionaryMin(dictionary):
    # pick the first
    m = ""
    for item in dictionary:
        m = item
        break
    # find the max
    for item in dictionary:
        if dictionary[item] < dictionary[m]:
            m = item
    return m

# returns the keys of the n smallest items in the dictionary
def DictionaryMinN(dictionary, n):
    d=dictionary.copy()
    keys = []
    for i in range(0,n):
        if(dictionary):
            key = DictionaryMin(d)
            keys.append(key)
            d.pop(key)
        else:
            break
    return keys

# returns the keys of the n largest items in the dictionary
def DictionaryMaxN(dictionary, n):
    d=dictionary.copy()
    keys = []
    for i in range(0,n):
        if(dictionary):
            key = DictionaryMax(d)
            keys.append(key)
            d.pop(key)
        else:
            break
    return keys
