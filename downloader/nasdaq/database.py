import time
from google.cloud import bigquery

class database():
    client = None


    def __init__(self):
        self.client = bigquery.Client()


    def setSchema(self, table):
        table.schema = (
            bigquery.table.SchemaField(name='Exchange', field_type='STRING'),
            bigquery.table.SchemaField(name='Symbol', field_type='STRING'),
            bigquery.table.SchemaField(name='Name', field_type='STRING'),
            bigquery.table.SchemaField(name='LastSale', field_type='FLOAT'),
            bigquery.table.SchemaField(name='MarketCap', field_type='FLOAT'),
            bigquery.table.SchemaField(name='IPOYear', field_type='INTEGER'),
            bigquery.table.SchemaField(name='Sector', field_type='STRING'),
            bigquery.table.SchemaField(name='Industry', field_type='STRING')
        )
        return table


    def create(self):
        table = self.client.dataset('downloader').table('symbols')
        if not table.exists():
            table = self.setSchema(table)
            table.create()


    def delete(self):
        table = self.client.dataset('downloader').table('symbols')
        if table.exists():
            table.delete()

            # Need to sleep - http://stackoverflow.com/questions/36415265/after-recreating-bigquery-table-streaming-inserts-are-not-working
            print('Going to sleep to give delete time to propagate.')
            time.sleep(30*60)


    def upload(self, filename):
        table = self.client.dataset('downloader').table('symbols')
        table = self.setSchema(table)
        with open(filename, 'rb') as readable:
            table.upload_from_file(readable, source_format='CSV')


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
