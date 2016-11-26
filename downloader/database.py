from google.cloud import bigquery

class database():
    client = None
    dataset = None
    table = None


    def __init__(self):
        self.client = bigquery.Client()
        self.dataset = self.client.dataset('downloader')
        self.table = self.dataset.table('symbols', schema)


    def delete(self):
        if self.table.exists():
            self.table.delete()


    def create(self):
        self.table.create()


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
