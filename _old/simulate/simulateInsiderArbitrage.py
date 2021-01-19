import datetime
import yahoo.sql
import edgar.sql
import google.sql
import math


def run():
    quoteSql = yahoo.sql.sql()
    edgarSql = edgar.sql.sql()
    googleSql = google.sql.sql()

    capital = 150 * 360
    holdings = []

    startDate = datetime.date.today() - datetime.timedelta(days=360)
    endDate = datetime.date.today()
    currentDate = startDate

    while currentDate < endDate:
        [capital, holdings] = runForDate(currentDate, capital, holdings, quoteSql, edgarSql, googleSql)
        printHoldings(capital, holdings, currentDate, quoteSql)
        currentDate = currentDate + datetime.timedelta(days=1)


def printHoldings(capital, holdings, currentDate, quoteSql):
    # print(currentDate.isoformat() + '\t' + str(currentDate.isoweekday()) +'\t$' + str(round(capital,2)))

    value = capital
    for holding in holdings:
        quote = quoteSql.fetchForSymbolAndDate(holding['Symbol'], currentDate)
        if quote:
            value = value + quote['Close'] * holding['Shares']
    if currentDate.weekday() < 5:  # check if this is a weekday - sat, sun are 5 and 6.
        print(value)
    # print(holdings)


def runForDate(currentDate, capital, holdings, quoteSql, edgarSql, googleSql):
    [capital, holdings] = buy(currentDate, capital, holdings, quoteSql, edgarSql, googleSql)
    # [capital, holdings] = sell(currentDate, capital, holdings, quoteSql, edgarSql, googleSql)
    return [capital, holdings]


def buy(currentDate, capital, holdings, quoteSql, edgarSql, googleSql):
    if currentDate.weekday() == 0:
        transactions = edgarSql.fetch(currentDate - datetime.timedelta(days=3))
    elif currentDate.weekday() == 1 or currentDate.weekday() == 2 or currentDate.weekday() == 3 or currentDate.weekday() == 4:
        transactions = edgarSql.fetch(currentDate - datetime.timedelta(days=1))
    elif currentDate.weekday() == 5 or currentDate.weekday() == 6:
        return [capital, holdings]

    if not transactions:
        return [capital, holdings]

    for transaction in transactions:
        if transactionIsABuy(transaction, holdings, currentDate, googleSql, quoteSql):
            holding = {}
            holding['Shares'] = math.floor(150 / transaction['TransactionPricePerShare'])
            holding['PricePerShare'] = transaction['TransactionPricePerShare']
            holding['Symbol'] = transaction['IssuerTradingSymbol']
            holdings.append(holding)
            capital = capital - (holding['Shares'] * holding['PricePerShare'])
            return [capital, holdings]

    return [capital, holdings]


def calculatePE(fundamentals):
    if fundamentals['EPS'] == 0:
        pe = 0
    else:
        pe = fundamentals['Open'] / fundamentals['EPS']
    return pe


def transactionIsABuy(transaction, holdings, currentDate, googleSql, quoteSql):
    # don't buy a symbol we already have
    for holding in holdings:
        if transaction['IssuerTradingSymbol'] == holding['Symbol']:
            return False

    fundamentals = googleSql.fetch(currentDate, transaction['IssuerTradingSymbol'])
    if not fundamentals:
        return False

    pe = calculatePE(fundamentals)
    if (pe > 8):
        return False

    quote = quoteSql.fetchForSymbolAndDate(transaction['IssuerTradingSymbol'], currentDate)
    if not quote:
        return False

    value = transaction['TransactionPricePerShare'] * transaction['TransactionShares']
    if value < 100000:
        return False

    buyPrice = transaction['TransactionPricePerShare']
    if buyPrice < quote['Low']:
        return False

    if quote['Low'] <= buyPrice:
        return True

    return False


run()
