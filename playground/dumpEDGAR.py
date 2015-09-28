import edgar.database
import google.database


def run():
    outputFile = open('/home/ec2-user/edgarOut.csv', 'w')
    outputFile.write('Symbol' + ',')
    outputFile.write('AcceptanceDatetime' + ',')
    outputFile.write('TransactionDate' + ',')
    outputFile.write('TransactionPricePerShare' + ',')
    outputFile.write('Close' + ',')
    outputFile.write('PE' + ',')
    outputFile.write('Yield' + ',')
    outputFile.write('RptOwnerName' + ',')
    outputFile.write('TransactionShares' + ',')
    outputFile.write('TradeValue' + ',')
    outputFile.write('SharesOwned' + ',')
    outputFile.write('TotalValue' + ',')
    outputFile.write('IsDirector' + ',')
    outputFile.write('IsOfficer' + ',')
    outputFile.write('IsTenPercentOwner' + ',')
    outputFile.write('IsOther' + '\n')

    import datetime
    currentDate = datetime.date(2014, 11, 26)

    form4DB = edgar.database.database()
    forms = form4DB.fetch(currentDate)

    fundamentalsDB = google.database.database()
    for form in forms:
        symbol = form['IssuerTradingSymbol']
        fundamentals = fundamentalsDB.fetch(currentDate, symbol)

        if fundamentals:
            pe = calculatePE(fundamentals)
            if marketPrice(form, fundamentalsDB):
                tradeValue = form['TransactionPricePerShare'] * form['TransactionShares']
                totalValue = form['TransactionPricePerShare'] * form[
                    'SharesOwned']  # maybe use close price for this instead?  not sure...

                # assuming a quarterly dividend (this could be wrong!)
                stockYield = str(round((fundamentals['Dividend'] / fundamentals['Close']) * 100 * 4, 2)) + '%'

                outputFile.write(symbol + ',')
                outputFile.write(str(form['AcceptanceDatetime']) + ',')
                outputFile.write(str(form['TransactionDate'].strftime('%Y-%m-%d')) + ',')
                outputFile.write(str(round(form['TransactionPricePerShare'], 2)) + ',')
                outputFile.write(str(round(fundamentals['Close'], 2)) + ',')
                outputFile.write(str(round(pe, 2)) + ',')
                outputFile.write(stockYield + ',')
                outputFile.write(form['RptOwnerName'] + ',')
                outputFile.write(str(int(form['TransactionShares'])) + ',')
                outputFile.write(str(round(tradeValue, 2)) + ',')
                outputFile.write(str(int(form['SharesOwned'])) + ',')
                outputFile.Write(str(round(totalValue, 2)) + ',')
                outputFile.write(form['IsDirector'] + ',')
                outputFile.write(form['IsOfficer'] + ',')
                outputFile.write(form['IsTenPercentOwner'] + ',')
                outputFile.write(form['IsOther'] + '\n')
    outputFile.close()


def marketPrice(form, fundamentalsDB):
    # returns true if low<price<high, otherwise false
    quote = fundamentalsDB.fetch(form['TransactionDate'], form['IssuerTradingSymbol'])

    if not quote:
        return False

    if quote['Low'] <= form['TransactionPricePerShare'] and quote['High'] >= form['TransactionPricePerShare']:
        return True

    return False


def calculatePE(fundamentals):
    if fundamentals['EPS'] == 0:
        pe = 0
    else:
        pe = fundamentals['Close'] / fundamentals['EPS']
    return pe


run()
