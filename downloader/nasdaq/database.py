from google.cloud import bigquery

class database():
    def __init__(self):
        bigquery_client = bigquery.Client()
        dataset_name = 'downloader'
        dataset = bigquery_client.dataset(dataset_name)
        dataset.create()
        print('Dataset {} created.'.format(dataset.name))

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
