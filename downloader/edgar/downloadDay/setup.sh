#!/usr/bin/env bash

role_arn="arn:aws:iam::675101987453:role/arbit_role"

# This script assumes a configured AWS CLI and that the role_arn above is set.
# (1) Create lambda functions for the downloader
# (2) Download old data
# (3) Setup jobs to download new nightly data

zip -r main.zip main.py

aws lambda create-function \
  --function-name downloadDay \
  --runtime python3.6 \
  --zip-file fileb://main.zip \
  --handler main.run \
  --role ${role_arn}

aws lambda update-function-code \
--function-name downloadDay \
--zip-file fileb://main.zip
