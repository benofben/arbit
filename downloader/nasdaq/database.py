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
        query = 'SELECT Symbol FROM downloader.symbols'
        query_results = client.run_sync_query(query)
        query_results.use_legacy_sql = False
        query_results.run()

        rows = query_results.fetch_data()
        for row in rows:
            print(row)

        symbols = []
        return symbols
