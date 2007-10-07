downloader:
Downloads all the symbols from Nasdaq, NYSE and AMER with market value > $1,000,000,000.  
These symbols are reformatted, the dates are changed to seconds since 1970.  Any symbol with an IPO after 1/1/2002 is discarded.

ValidateL picks the window paramter for the L (gain) predictor.
Simulate trys my current strategy on the historic data.
Run picks stocks for tomorrow.  This invokes the downloader, so it'll kill the existing data directory.

GetData is a helper module.  It pulls stuff from the data directory.
Predictors is a helper module.  Both Simulate and Run use it.  It contains L and K.