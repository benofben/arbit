#!/usr/bin/env bash

role_arn="arn:aws:iam::675101987453:role/arbit_role"

rm main.zip
zip -r main.zip *.py

aws lambda delete-function \
  --function-name downloader-edgar-form4

aws lambda create-function \
  --function-name downloader-edgar-form4 \
  --runtime python3.6 \
  --zip-file fileb://main.zip \
  --handler main.run \
  --role ${role_arn}
