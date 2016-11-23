from google.cloud import bigquery

class database():
    def __init__(self):
        bigquery_client = bigquery.Client()
        dataset = bigquery_client.dataset('downloader')
        table = dataset.table('symbols')

        if table.exists():
            table.delete()

        field1 = bigquery.table.SchemaField(name='Symbol', field_type='STRING')
        field2 = bigquery.table.SchemaField(name='Exchange', field_type='STRING')
        field3 = bigquery.table.SchemaField(name='Name', field_type='STRING')
        field4 = bigquery.table.SchemaField(name='LastSale', field_type='FLOAT')
        field5 = bigquery.table.SchemaField(name='MarketCap', field_type='FLOAT')
        field6 = bigquery.table.SchemaField(name='IPOYear', field_type='INTEGER')
        field7 = bigquery.table.SchemaField(name='Sector', field_type='STRING')
        field8 = bigquery.table.SchemaField(name='Industry', field_type='STRING')
        schema = [field1, field2, field3, field4, field5, field6, field7, field8]
        table.create(schema=schema)

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
