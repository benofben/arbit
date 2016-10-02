#arbit

Arbit has been an effort to apply some sort of statistical arbitrage to the equity and futures markets.  The orginal code was in Mathematica, written during a Christmas vacation in 2006.  It was ported to Matlab and later Python.  I moved it to python3 well before that was a viable language, back in the Python 3K days.  After that, the code was modified to use Oracle and I had to custom build the cx_Oracle driver.  By 2015, it used python3, mongodb and ran on AWS.

I'm currently in the process of dumping all the data to BigQuery.  After that is complete, I'd like to look at using AppEngine or something similar to host the scripts rather than running on IaaS.
