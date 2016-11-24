#arbit

Arbit has been an effort to apply some sort of statistical arbitrage to the equity and futures markets.  

## History
The original code was in Mathematica, written during a Christmas vacation in 2006.  It was ported to Matlab and later Python.  I moved it to python3 well before that was a viable language, back in the Python 3K days.  At one point it had a network bootable OS image and ran on a small cluster in my London apartment.  

There was a brief, glorious, period in there where the API integration to TD Ameritrade all worked and the model was spitting out predictions with high confidence that netted $1-2k/day.  Then the market changed and prediction confidence plunged.

Sometime after that, the code was modified to use Oracle and I had to custom build the cx_Oracle driver.  By 2015, it used python3, mongodb and ran on AWS.  It also included a little PHP and d3 visualization.

## Roadmap
I'm currently in the process of refactoring to BigQuery.  After that is complete, I'd like to look at using AppEngine or something similar to host the scripts rather than running on IaaS.  I'm also very curious to take a closer look at Cloud ML and Cloud Datalab.  Depending on how that goes, I may automate connectivity to Interactive Brokers again.
