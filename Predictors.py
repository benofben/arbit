def NDayHigh(quotes, day):
    nDayHigh = 0
    Close = quotes["Close"][day]

    for d in range(day-2, -1, -1):
        High = quotes["High"][d]
        if(Close>High):
            nDayHigh = nDayHigh + 1
        else:
            break
    return nDayHigh

def NDayLow(quotes, day):
    nDayLow = 0
    Close = quotes["Close"][day]

    for d in range(day-2, -1, -1):
        Low = quotes["Low"][d]
        if(Close<Low):
            nDayLow = nDayLow + 1
        else:
            break
    return nDayLow

def DailyChange(quotes, day):
    TodayClose = quotes["Close"][day-1]
    YesterDayClose = quotes["Close"][day-2]
    return TodayClose / YesterDayClose

def ExpectedReturn(quotes, day, window, take):
    e = 1.0;
    for d in range(day-window, day):
        Open = quotes["Open"][d]
        High = quotes["High"][d]
        Close = quotes["Close"][d]
        
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
def L(quotes, day, window, take):
    wins = 0.0
    total = 0

    for d in range(day-window, day):
        Open = quotes["Open"][d]
        High = quotes["High"][d]
        if(High >= Open * take):
            wins = wins + 1
        total = total + 1

    return wins / total

# loss function
def K(quotes, day, window, take):
    loss = 1.0
    total = 0
    
    for d in range(day-window, day):
        Open = quotes["Open"][d]
        High = quotes["High"][d]
        Close = quotes["Close"][d]
        if(High < Open * take):
            loss = loss * (Close / Open)
            total = total + 1

    import math
    loss = math.pow (loss, 1.0/total)
    
    return loss

# returns the key of the smallest item in the dictionary
def DictionaryMax(dictionary):
    m=""
    # pick the first key
    for key in dictionary:
        m = key
        break
    # find the max
    for key in dictionary:
        if dictionary[key] > dictionary[m]:
            m = key
    return m

# returns the key of the largest item in the dictionary
def DictionaryMin(dictionary):
    m=""
    # pick the first key
    for key in dictionary:
        m = key
        break
    # find the min
    for key in dictionary:
        if dictionary[key] < dictionary[m]:
            m = key
    return m

# returns the keys of the n smallest items in the dictionary
def DictionaryMinN(dictionary, n):
    d=dictionary.copy()
    keys = []
    for i in range(0,n):
        if(d):
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
        if(d):
            key = DictionaryMax(d)
            keys.append(key)
            d.pop(key)
        else:
            break
    return keys
