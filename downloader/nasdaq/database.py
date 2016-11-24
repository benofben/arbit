from google.cloud import bigquery

class database():
    table = None


    def __init__(self):
        bigquery_client = bigquery.Client()
        dataset = bigquery_client.dataset('downloader')
        self.table = dataset.table('symbols')


    def create(self):
        if not self.table.exists():
            self.table.schema = (
                bigquery.table.SchemaField(name='Exchange', field_type='STRING'),
                bigquery.table.SchemaField(name='Symbol', field_type='STRING'),
                bigquery.table.SchemaField(name='Name', field_type='STRING'),
                bigquery.table.SchemaField(name='LastSale', field_type='FLOAT'),
                bigquery.table.SchemaField(name='MarketCap', field_type='FLOAT'),
                bigquery.table.SchemaField(name='IPOYear', field_type='INTEGER'),
                bigquery.table.SchemaField(name='Sector', field_type='STRING'),
                bigquery.table.SchemaField(name='Industry', field_type='STRING')
            )
            self.table.create()


    def delete(self):
        if self.table.exists():
            self.table.delete()


    def upload(self, filename):
        with open(filename, 'rb') as readable:
            self.table.upload_from_file(readable, source_format='CSV', skip_leading_rows=1)


    def getSymbols(self):
        #query = 'SELECT * FROM downloader.symbols'
        #job = bigquery.job.
        #result =

        for row in self.table.fetch_data():
            print(row)

        symbols = []
        return symbols
