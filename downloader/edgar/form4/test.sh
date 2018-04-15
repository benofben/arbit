#!/usr/bin/env bash

aws lambda invoke \
  --invocation-type RequestResponse \
  --function-name downloader-edgar-form4 \
  --payload '{"url":"https://www.sec.gov/Archives/edgar/data/1035927/0001664015-18-000004.txt"}' \
  output.txt
