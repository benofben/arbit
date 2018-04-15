aws lambda invoke \
  --invocation-type RequestResponse \
  --function-name edgar-download-day \
  --payload '{"date":"2018-04-02"}' \
  outputfile.txt
