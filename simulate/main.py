import datetime
import quotes
quotes = quotes.run()

def run():
    capital = 25000

    startDate = datetime.date.today() - datetime.timedelta(days = 360 * 3)
    endDate = datetime.date.today()
    currentDate = startDate

    while currentDate < endDate:
        return

#        [capital, bestSymbol] = runForDate(capital, currentDate, quotes, symbols)
#        print(str(currentDate) + ',' + str(capital) + ',' + str(bestSymbol))
#        currentDate = currentDate + datetime.timedelta(days=1)


def runForDate(capital, currentDate, quotes, symbols):
    bestSymbol = None
    if currentDate.weekday() < 5:
        bestSymbol = getBestSymbolForDate(currentDate, quotesDB, symbols)
        if bestSymbol:
            r = simulateReturnForDate(currentDate, bestSymbol, quotesDB)
            capital *= r
    capital = round(capital, 2)
    return [capital, bestSymbol]


def getBestSymbolForDate(currentDate, quotesDB, symbols):
    bestSymbol = None
    bestPWin = 0

    for symbol in symbols:
        #		pWin = getPWin(currentDate, symbol, quotesDB)
        pWin = getExpectedReturn(currentDate, symbol, quotesDB)
        if pWin > bestPWin:
            bestPWin = pWin
            bestSymbol = symbol

    return bestSymbol


def simulateReturnForDate(currentDate, symbol, quotesDB):
    r = 1.0
    quote = quotesDB.findQuoteForDate(currentDate, symbol)

    if quote:
        h = quote['High']
        o = quote['Open']
        c = quote['Close']

        if h > o * 1.01:
            r = 1.01
        else:
            r = c / o

    return r


def getPWin(currentDate, symbol, quotesDB):
    window = 30
    quotes = quotesDB.findSubquoteForSymbolWithWindow(symbol, currentDate, window)

    wins = 0.0
    total = 0.0

    for q in quotes:
        if q['High'] > q['Open'] * 1.01:
            wins += 1.0
        total += 1.0

    if (total == 0):
        return 0.0
    return wins / total


def getExpectedReturn(currentDate, symbol, quotesDB):
    window = 20
    quotes = quotesDB.findSubquoteForSymbolWithWindow(symbol, currentDate, window)

    e = 1.0
    for q in quotes:
        # We're getting data back where the close>high.
        # This shouldn't be possible.
        # Going to skip data like that.
        if (q['High'] < q['Close']):
            pass
        else:
            if q['High'] > q['Open'] * 1.01:
                e *= 1.01
            else:
                e *= q['Close'] / q['Open']
    return e


run()
