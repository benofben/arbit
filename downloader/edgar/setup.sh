#!/usr/bin/env bash

# Setup DynamoDB

aws dynamodb create-table \
  --attribute-definitions <value> \
  --table-name downloader-edgar-form4-transactions \
  --key-schema <value>

# Setup Lambda

cd day
./setup.sh
cd ..

cd form4
./setup.sh
cd ..
