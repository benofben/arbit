import datetime
import edgar

def run():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    edgar.downloadDate(yesterday)

run()
