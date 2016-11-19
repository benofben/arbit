from pymongo import MongoClient


class database():
    def __init__(self):
        pass

    def dropCollection(self):
        pass

    def __del__(self):
        pass

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
        pass

    def getAllSymbols(self):
        symbols = []
        #for symbolInformation in self.client.arbit.symbols.find():
        #    symbols.append(symbolInformation['Symbol'])
        return symbols
