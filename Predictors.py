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
