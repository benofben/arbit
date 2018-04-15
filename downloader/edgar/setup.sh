#!/usr/bin/env bash

# Setup DynamoDB

aws dynamodb create-table \
  --attribute-definitions <value> \
  --table-name downloader-edgar-form4-transactions \
  --key-schema <value>

  --attribute-definitions \
      AttributeName=Artist,AttributeType=S \
      AttributeName=SongTitle,AttributeType=S \
  --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE \



# Setup Lambda

cd day
./setup.sh
cd ..

cd form4
./setup.sh
cd ..
