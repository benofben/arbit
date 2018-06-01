# downloader

## EDGAR

EDGAR now uses HTTP for access.  A writeup on that is [here](https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm).

To start the downloader for the first time run:

    cd arbit/downloader/edgar
    screen -S edgar python3 downloadAll.py

To start the nightly job run:

    cd arbit/downloader/edgar
    screen -S edgar python3 downloader.py
