import edgar.database
import google.database
    
def run(currentDate):
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
                totalValue = form['TransactionPricePerShare'] * form['SharesOwned'] #maybe use close price for this instead?  not sure...
    
                # assuming a quarterly dividend (this could be wrong!)
                stockYield = str(round((fundamentals['Dividend']/fundamentals['Close'])*100*4,2))+'%'
                    
                acceptanceDateTimeString = '<a href="http://54.87.46.23/index.php?symbol=' + symbol + '">' +  str(form['AcceptanceDatetime']) + '</a>' 
                symbolString = '<a href="http://www.google.com/finance?q=' + symbol + '">' + symbol +'</a>'
                s+='<tr><td>' + acceptanceDateTimeString + '</td><td>' + str(form['TransactionDate'].strftime('%Y-%m-%d')) + '</td><td>' + symbolString + '</td><td>' + '$' + str(round(form['TransactionPricePerShare'],2)) + '</td><td>' + '$' + str(round(fundamentals['Close'],2)) + '</td><td>' + str(round(pe,2)) + '</td><td>' + stockYield + '</td><td>' + form['RptOwnerName'] + '</td><td>' + str(int(form['TransactionShares'])) + '</td><td>' + '$' + str(round(tradeValue,2)) + '</td><td>' + str(int(form['SharesOwned'])) + '</td><td>' + '$' + str(round(totalValue,2))
                s+= '</td><td>' + form['IsDirector'] + '</td><td>' + form['IsOfficer'] + '</td><td>' + form['IsTenPercentOwner'] + '</td><td>' + form['IsOther']
                s+='</td></tr>'

def marketPrice(form, fundamentalsDB):
    #returns true if low<price<high, otherwise false
    quote = fundamentalsDB.fetch(form['TransactionDate'], form['IssuerTradingSymbol'])
    
    if not quote:
        return False
    
    if quote['Low']<=form['TransactionPricePerShare'] and quote['High']>=form['TransactionPricePerShare']:
        return True
    
    return False

def calculatePE(fundamentals):
    if fundamentals['EPS']==0:
        pe = 0
    else:
        pe = fundamentals['Close']/fundamentals['EPS']
    return pe

run()