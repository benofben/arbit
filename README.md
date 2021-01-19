# arbit

Arbit has been an effort to apply some sort of statistical arbitrage to the equity and futures markets.  

## History
The original code was in Mathematica, written during a Christmas vacation in 2006.  It was ported to Matlab and later Python.  I moved it to python3 well before that was a viable language, back in the Python 3K days.  At one point it had a network bootable OS image and ran on a small cluster under a desk in my London apartment.  

There was a brief, glorious, period in there around 2008 where the API integration to TD Ameritrade all worked and the model (Naive Bayes with a lot of featurization logic) was spitting out predictions with high confidence that netted $1-2k/day.  Then the market changed and prediction confidence plunged.

Sometime after that, the code was modified to use Oracle and I had to custom build the cx_Oracle driver.  By 2015, it used python3, mongodb and ran on AWS.  It also included a little PHP and d3 visualization.

During 2016, I rewrote it to use GCP BigQuery and AppEngine.  At the time there were a lot of issues with the BigQuery driver and it seemed like pure serverless wasn't quite there as AppEngine was missing various language features and isn't serverless anyway.  The goal at the time was to use Cloud ML and Cloud Datalab.  In 2018, Cloud Functions looked like a solution but they were still in beta and only supported node.js.

In November 2017, AWS came out with Sagemaker.  Between that, S3, Lambda and Athena, it seemed like giving the AWS ecosystem a try was in order.  It turned out Lambda has a 5 minute limit on function duration.  That's because it's a synchronous request/reply model.  That then cascaded into a nightmarish architecture that would require Lambda, SNS/SQS, DynamoDB, EMR and S3 all to ETL some files around.  Given all that, I decided we're too early for serverless.

In 2018, I tried to stand all this up on GCP.  Therein I discovered the BigQuery driver had some issues.

## Current
Just fiddling on my laptop like the good old days.  This will probably quickly move to a GCP VM.

I grabbed a list of S&P 500 symbols from here: https://github.com/datasets/s-and-p-500-companies/blob/master/data/constituents_symbols.txt

I'm using Yahoo for quote data again.
