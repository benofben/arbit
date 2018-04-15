#!/usr/bin/env bash

aws lambda invoke \
  --invocation-type RequestResponse \
  --function-name downloader-edgar-day \
  --payload '{"date":"2018-04-02"}' \
  output.txt
