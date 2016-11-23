from google.cloud import bigquery

class database():
    table = ''

    def __init__(self):
        bigquery_client = bigquery.Client()
        dataset = bigquery_client.dataset('downloader')
        table = dataset.table('symbols')

        if table.exists():
            table.delete()

        table.schema = (
            bigquery.table.SchemaField(name='Symbol', field_type='STRING'),
            bigquery.table.SchemaField(name='Exchange', field_type='STRING'),
            bigquery.table.SchemaField(name='Name', field_type='STRING'),
            bigquery.table.SchemaField(name='LastSale', field_type='FLOAT'),
            bigquery.table.SchemaField(name='MarketCap', field_type='FLOAT'),
            bigquery.table.SchemaField(name='IPOYear', field_type='INTEGER'),
            bigquery.table.SchemaField(name='Sector', field_type='STRING'),
            bigquery.table.SchemaField(name='Industry', field_type='STRING')
        )
        table.create()


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
        rows = []
        table.insert_data(rows)


    def getAllSymbols(self):
        symbols = []
        #for symbolInformation in self.client.arbit.symbols.find():
        #    symbols.append(symbolInformation['Symbol'])
        return symbols
