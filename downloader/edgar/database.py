from google.cloud import bigquery
import datetime

class database():
    client = None
    dataset = None
    table = None


    def __init__(self):
        self.client = bigquery.Client()
        self.dataset = self.client.dataset('downloader')
        schema = (
            bigquery.table.SchemaField(name='SecDocument', field_type='STRING'),
            bigquery.table.SchemaField(name='AcceptanceDatetime', field_type='DATETIME'),
            bigquery.table.SchemaField(name='IssuerTradingSymbol', field_type='STRING'),
            bigquery.table.SchemaField(name='RptOwnerCik', field_type='STRING'),
            bigquery.table.SchemaField(name='RptOwnerName', field_type='STRING'),
            bigquery.table.SchemaField(name='IsDirector', field_type='BOOLEAN'),
            bigquery.table.SchemaField(name='IsOfficer', field_type='BOOLEAN'),
            bigquery.table.SchemaField(name='IsTenPercentOwner', field_type='BOOLEAN'),
            bigquery.table.SchemaField(name='IsOther', field_type='BOOLEAN'),
            bigquery.table.SchemaField(name='TransactionDate', field_type='DATE'),
            bigquery.table.SchemaField(name='TransactionShares', field_type='FLOAT'),
            bigquery.table.SchemaField(name='TransactionPricePerShare', field_type='FLOAT'),
            bigquery.table.SchemaField(name='TransactionAcquired', field_type='BOOLEAN'),
            bigquery.table.SchemaField(name='SharesOwned', field_type='FLOAT')
        )
        self.table = self.dataset.table('form4', schema)


    def create(self):
        if not self.table.exists():
            self.table.create()


    def insert(self, form4Information):
        year = form4Information['acceptanceDatetime'][0:4]
        month = form4Information['acceptanceDatetime'][4:6]
        day = form4Information['acceptanceDatetime'][6:8]
        hour = form4Information['acceptanceDatetime'][8:10]
        minute = form4Information['acceptanceDatetime'][10:12]
        second = form4Information['acceptanceDatetime'][12:14]
        acceptanceDatetime = year + '-' + month + '-' + day + 'T' + hour + ':' + minute + ':' + second

        year = form4Information['transactionDate'][0:4]
        month = form4Information['transactionDate'][5:7]
        day = form4Information['transactionDate'][8:10]
        transactionDate = year + '-' + month + '-' + day

        if(form4Information['transactionAcquiredDisposedCode']=='A'):
            transactionAcquired = True
        else:
            transactionAcquired = False

        row = (
            form4Information['secDocument'],
            acceptanceDatetime,
            form4Information['issuerTradingSymbol'],
            form4Information['rptOwnerCik'],
            form4Information['rptOwnerName'],
            form4Information['isDirector'],
            form4Information['isOfficer'],
            form4Information['isTenPercentOwner'],
            form4Information['isOther'],
            transactionDate,
            form4Information['transactionShares'],
            form4Information['transactionPricePerShare'],
            transactionAcquired,
            form4Information['sharesOwned'],
        )
        rows=[row]
        print(rows)
        result = self.table.insert_data(rows)
        print(result)
