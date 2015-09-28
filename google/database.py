from pymongo import MongoClient
import datetime


class database():
    def __init__(self):
        self.client = MongoClient()

    def __del__(self):
        self.client.disconnect()

    def insert(self, fundamentals):
        f = {
            'Symbol': fundamentals['Symbol'],
            'DownloadDate': fundamentals['Date'],
            'Dividend': fundamentals['Dividend'],
            'EPS': fundamentals['EPS'],
            'Shares': fundamentals['Shares'],
            'InstitutionalOwnership': fundamentals['InstitutionalOwnership'],
            'Open': fundamentals['Open'],
            'High': fundamentals['High'],
            'Low': fundamentals['Low'],
            'Close': fundamentals['Close'],
        }
        self.client.arbit.fundamentals.insert(f)

    def fetch(self, currentDate, symbol):
        d = currentDate
        startDatetime = datetime.datetime(d.year, d.month, d.day, 0, 0, 0)
        endDatetime = datetime.datetime(d.year, d.month, d.day, 23, 59, 59)

        for result in self.client.arbit.fundamentals.find(
                {'Symbol': symbol, 'DownloadDate': {'$gte': startDatetime, '$lt': endDatetime}}):
            return (result)
        return ([])
