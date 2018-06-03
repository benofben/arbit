from google.cloud import bigquery
import google.api_core.exceptions

client = bigquery.Client()
dataset_ref = client.dataset('downloader')
table_ref = dataset_ref.table('form4')

schema = [
    bigquery.SchemaField('SecDocument', 'STRING'),
    bigquery.SchemaField('AcceptanceDatetime', 'DATETIME'),
    bigquery.SchemaField('IssuerTradingSymbol', 'STRING'),
    bigquery.SchemaField('RptOwnerCik', 'STRING'),
    bigquery.SchemaField('RptOwnerName', 'STRING'),
    bigquery.SchemaField('IsDirector', 'BOOLEAN'),
    bigquery.SchemaField('IsOfficer', 'BOOLEAN'),
    bigquery.SchemaField('IsTenPercentOwner', 'BOOLEAN'),
    bigquery.SchemaField('IsOther', 'BOOLEAN'),
    bigquery.SchemaField('TransactionDate', 'DATE'),
    bigquery.SchemaField('TransactionShares', 'FLOAT'),
    bigquery.SchemaField('TransactionPricePerShare', 'FLOAT'),
    bigquery.SchemaField('TransactionAcquired', 'BOOLEAN'),
    bigquery.SchemaField('SharesOwned', 'FLOAT')
]

table = bigquery.Table(table_ref, schema=schema)

# Create the table or pass if it already exists
try:
    table = client.create_table(table)
except google.api_core.exceptions.Conflict:
    pass

assert table.table_id == 'form4'

table = client.get_table(table_ref)

row = (
    'secDocument',
    'acceptanceDatetime',
    'issuerTradingSymbol',
    'rptOwnerCik',
    'rptOwnerName',
    'isDirector',
    'isOfficer',
    'isTenPercentOwner',
    'isOther',
    'transactionDate',
    'transactionShares',
    'transactionPricePerShare',
    'transactionAcquired',
    'sharesOwned',
)

rows_to_insert = [row]
errors = client.insert_rows(table, rows_to_insert)
assert errors == []
