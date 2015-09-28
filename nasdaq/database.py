from pymongo import MongoClient


class database():
    def __init__(self):
        self.client = MongoClient()

    def dropCollection(self):
        self.client.arbit.symbols.drop()

    def __del__(self):
        self.client.disconnect()

    def insert(self, symbolInformation):
        symbol = {
            'Symbol': symbolInformation['Symbol'],
            'Exchange': symbolInformation['Exchange'],
            'Name': symbolInformation['Name'],
            'LastSale': symbolInformation['LastSale'],
            'MarketCap': symbolInformation['MarketCap'],
            'IPOYear': symbolInformation['IPOYear'],
            'Sector': symbolInformation['Sector'],
            'Industry': symbolInformation['Industry']
        }
        self.client.arbit.symbols.insert(symbol)

    def getAllSymbols(self):
        symbols = []
        for symbolInformation in self.client.arbit.symbols.find():
            symbols.append(symbolInformation['Symbol'])
        return symbols
