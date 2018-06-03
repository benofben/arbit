# arbit/downloader/edgar

EDGAR now uses HTTP for access.  A writeup on that is [here](https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm).

## Setup

To start the EDGAR downloader run this:

    cd ~/arbit/downloader/edgar
    screen -S edgar
    python3 downloader.py

Then type ^ad to detach.

To get historical data, you'll need to start one of these too:

    screen -S edgar-historical
    python3 downloadAll.py

Then type ^ad to detach.
