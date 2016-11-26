from google.cloud import bigquery

class database():
    client = None


    def __init__(self):
        self.client = bigquery.Client()


    def getSchema(self):
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
        return schema


    def create(self):
        dataset = self.client.dataset('downloader')
        table = dataset.table('symbols', self.getSchema())
        assert not table.exists()
        table.create()
        assert table.exists()


    def delete(self):
        dataset = self.client.dataset('downloader')
        table = dataset.table('symbols', self.getSchema())
        assert table.exists()
        table.delete()
        assert not table.exists()


    def upload(self, filename):
        dataset = self.client.dataset('downloader')
        table = dataset.table('symbols', self.getSchema())
        with open(filename, 'rb') as readable:
            table.upload_from_file(readable, source_format='CSV')


    def getSymbols(self):
        query = 'SELECT Symbol FROM downloader.symbols'
        query_results = self.client.run_sync_query(query)
        query_results.use_legacy_sql = False
        query_results.run()
        assert query.complete
        [rows, unused_total_rows, unused_page_token] = query_results.fetch_data()
        symbols = []
        for row in rows:
            symbols.append(row[0])
        return symbols
