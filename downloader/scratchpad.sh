aws lambda invoke \
  --invocation-type RequestResponse \
  --function-name add \
  --payload '{"a":1, "b":2 }' \
  outputfile.txt
