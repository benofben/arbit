import datetime
from google.cloud import bigquery

class database():
    client = None


    def __init__(self):
        self.client = bigquery.Client()


    def setSchema(self, table):
        table.schema = (
            bigquery.table.SchemaField(name='Symbol', field_type='STRING'),
            bigquery.table.SchemaField(name='Date', field_type='DATE'),
            bigquery.table.SchemaField(name='Open', field_type='FLOAT'),
            bigquery.table.SchemaField(name='High', field_type='FLOAT'),
            bigquery.table.SchemaField(name='Low', field_type='FLOAT'),
            bigquery.table.SchemaField(name='Close', field_type='FLOAT'),
            bigquery.table.SchemaField(name='Volume', field_type='INTEGER'),
            bigquery.table.SchemaField(name='AdjustedClose', field_type='FLOAT')
        )
        return table


    def create(self):
        table = self.client.dataset('downloader').table('quotes')
        if not table.exists():
            table = self.setSchema(table)
            table.create()


    def delete(self):
        table = self.client.dataset('downloader').table('quotes')
        if table.exists():
            table.delete()


    def upload(self, filename):
        table = self.client.dataset('downloader').table('quotes')
        table = self.setSchema(table)
        with open(filename, 'rb') as readable:
            table.upload_from_file(readable, source_format='CSV', skip_leading_rows=1)
