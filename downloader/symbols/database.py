from google.cloud import bigquery

class database():
    client = None
    dataset = None
    table = None


    def __init__(self):
        self.client = bigquery.Client()
        self.dataset = self.client.dataset('downloader')
        schema = (
            bigquery.table.SchemaField(name='Exchange', field_type='STRING'),
            bigquery.table.SchemaField(name='Symbol', field_type='STRING'),
            bigquery.table.SchemaField(name='Name', field_type='STRING'),
            bigquery.table.SchemaField(name='LastSale', field_type='FLOAT'),
            bigquery.table.SchemaField(name='MarketCap', field_type='FLOAT'),
            bigquery.table.SchemaField(name='IPOYear', field_type='INTEGER'),
            bigquery.table.SchemaField(name='Sector', field_type='STRING'),
            bigquery.table.SchemaField(name='Industry', field_type='STRING')
        )
        self.table = self.dataset.table('symbols', schema)


    def create(self):
        assert not self.table.exists()
        self.table.create()
        assert self.table.exists()


    def delete(self):
        assert self.table.exists()
        self.table.delete()
        assert not self.table.exists()


    def upload(self, filename):
        with open(filename, 'rb') as readable:
            self.table.upload_from_file(readable, source_format='CSV', skip_leading_rows=1)


    def getSymbols(self):
        query = 'SELECT Symbol FROM downloader.symbols'
        query_results = self.client.run_sync_query(query)
        query_results.use_legacy_sql = False
        query_results.run()
        [rows, unused_total_rows, unused_page_token] = query_results.fetch_data()
        symbols = []
        for row in rows:
            symbols.append(row[0])
        return symbols
