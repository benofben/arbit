# arbit/downloader/edgar

EDGAR now uses HTTP for access.  A writeup on that is [here](https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm).

## Setup

We're going to need to create a VM to run the download.  The f1-micro costs $3.88 a month with the sustained use discount, so it's unlikely to break the bank.  Spin one of those up from the cloud shell with the command:

    gcloud compute instances create downloader-edgar \
      --zone us-east1-b \
      --machine-type f1-micro

Your environment is now woefully inadequate.  To fix it do this:

    sudo apt update
    sudo apt -y install git-all
    sudo apt -y install python3 python3-dev python3-pip
    pip3 install --upgrade google-cloud

To start the EDGAR downloader run this:

    git clone https://github.com/benofben/arbit.git
    cd arbit/downloader/edgar
    screen -S edgar
    python3 downloader.py

Then type ^ad to detach.

To get historical data, you'll need to start one of these too:

    cd arbit/downloader/edgar
    screen -S edgar-historical
    python3 downloadAll.py

Then type ^ad to detach.
