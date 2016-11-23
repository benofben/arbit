from google.cloud import bigquery

class database():
    table = ''
    rows = []


    def __init__(self):
        bigquery_client = bigquery.Client()
        dataset = bigquery_client.dataset('downloader')
        self.table = dataset.table('symbols')

        if self.table.exists():
            self.table.delete()

        self.table.schema = (
            bigquery.table.SchemaField(name='Symbol', field_type='STRING'),
            bigquery.table.SchemaField(name='Exchange', field_type='STRING'),
            bigquery.table.SchemaField(name='Name', field_type='STRING'),
            bigquery.table.SchemaField(name='LastSale', field_type='FLOAT'),
            bigquery.table.SchemaField(name='MarketCap', field_type='FLOAT'),
            bigquery.table.SchemaField(name='IPOYear', field_type='INTEGER'),
            bigquery.table.SchemaField(name='Sector', field_type='STRING'),
            bigquery.table.SchemaField(name='Industry', field_type='STRING')
        )
        self.table.create()


    def addRow(self, symbolInformation):
        row = (
            symbolInformation['Symbol'],
            symbolInformation['Exchange'],
            symbolInformation['Name'],
            symbolInformation['LastSale'],
            symbolInformation['MarketCap'],
            symbolInformation['IPOYear'],
            symbolInformation['Sector'],
            symbolInformation['Industry']
        )
        self.rows.append(row)


    def insert(self):
        self.table.insert_data(self.rows)


    def getAllSymbols(self):
        symbols = []
        #for symbolInformation in self.client.arbit.symbols.find():
        #    symbols.append(symbolInformation['Symbol'])
        return symbols
