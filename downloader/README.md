# downloader

The SEC used to provide access to EDGAR via FTP.  They've dropped that and it seems to be HTTP now.  A writeup on that is [here](https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm).

The root for the http access is [here](https://www.sec.gov/Archives/edgar/daily-index/).

Here's an example json file: https://www.sec.gov/Archives/edgar/daily-index/2018/QTR2/index.json

That links index files like this: https://www.sec.gov/Archives/edgar/daily-index/2018/QTR2/form.20180402.idx

# Setup

Just run this:

    cd downloader
    ./setup.sh
