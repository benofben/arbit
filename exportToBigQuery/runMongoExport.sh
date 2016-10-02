#!/usr/bin/env bash

mongoexport --db arbit --collection form4 --out form4.json
mongoexport --db arbit --collection fundamentals --out fundamentals.json
mongoexport --db arbit --collection ratingsChanges --out ratingsChanges.json
mongoexport --db arbit --collection symbols --out symbols.json
mongoexport --db arbit --collection yahooQuotes --out yahooQuotes.json

# reformat the json in a way BigQuery will like
python3 convertToBigQueryFormat.py

# copy everything to a bucket so we can import it to BigQuery
gsutil cp *.bigquery gs://mongoexport

# load the data into BigQuery
bq load --schema=form4_schema.json arbit.form4 gs://mongoexport/form4.json.bigquery
bq load --schema=fundamentals_schema.json arbit.fundamentals gs://mongoexport/fundamentals.json.bigquery
bq load --schema=ratingsChanges_schema.json arbit.ratingsChanges gs://mongoexport/ratingsChanges.json.bigquery
bq load --schema=symbols_schema.json arbit.symbols gs://mongoexport/symbols.json.bigquery
bq load --schema=yahooQuotes_schema.json arbit.yahooQuotes gs://mongoexport/yahooQuotes.json.bigquery
