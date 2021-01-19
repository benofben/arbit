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
bq load --schema=schemas/fundamentals_schema.json arbit.fundamentals gs://mongoexport/fundamentals.json.bigquery
bq load --schema=schemas/ratingsChanges_schema.json arbit.ratingsChanges gs://mongoexport/ratingsChanges.json.bigquery
bq load --schema=schemas/symbols_schema.json arbit.symbols gs://mongoexport/symbols.json.bigquery
bq load --schema=schemas/yahooQuotes_schema.json arbit.yahooQuotes gs://mongoexport/yahooQuotes.json.bigquery
