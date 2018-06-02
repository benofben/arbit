import datetime
import edgar

def run():
    date = datetime.date.today()

    while date > datetime.date(1,1,2000):
        date = date - datetime.timedelta(days=1)
        print(date)
        #edgar.downloadDate(date)

run()
