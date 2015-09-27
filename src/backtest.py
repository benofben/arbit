import yahoo.database
import datetime

quoteDB = yahoo.database.database()

filename='/home/ec2-user/sk/testPredictions.csv'
f=open(filename,'r')

capital=10000
for line in f:
    [d,symbol,p]=line.split(',')
    p=float(p)
    d=d.split('-')
    dt = datetime.datetime(int(d[0]),int(d[1]),int(d[2]))
    quote = quoteDB.findQuoteForDate(dt, symbol)
 
    if p>0 and quote:
        if quote['High']/quote['Open']>1.02:
            capital*=1.02
        else:
            capital*=quote['Close']/quote['Open']
        print(str(capital) + ' ' + symbol)