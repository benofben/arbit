from google.cloud import bigquery

class database():
    client = None
    dataset = None
    table = None


    def __init__(self):
        self.client = bigquery.Client()
        self.dataset = self.client.dataset('downloader')
        schema = (
            bigquery.table.SchemaField(name='Symbol', field_type='STRING'),
            bigquery.table.SchemaField(name='Date', field_type='DATE'),
            bigquery.table.SchemaField(name='Open', field_type='FLOAT'),
            bigquery.table.SchemaField(name='High', field_type='FLOAT'),
            bigquery.table.SchemaField(name='Low', field_type='FLOAT'),
            bigquery.table.SchemaField(name='Close', field_type='FLOAT'),
            bigquery.table.SchemaField(name='Shares', field_type='INTEGER'),
            bigquery.table.SchemaField(name='EPS', field_type='FLOAT'),
            bigquery.table.SchemaField(name='InstitutionalOwnership', field_type='FLOAT'),
            bigquery.table.SchemaField(name='Dividend', field_type='FLOAT')
        )
        self.table = self.dataset.table('fundamentals', schema)


    def create(self):
        if not self.table.exists():
            self.table.create()


    def upload(self, filename):
        with open(filename, 'rb') as readable:
            self.table.upload_from_file(readable, source_format='CSV', skip_leading_rows=0)
