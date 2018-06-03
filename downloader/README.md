# arbit/downloader

## Setup

We're going to need to create a VM to run the download.  The f1-micro costs $3.88 a month with the sustained use discount, so it's unlikely to break the bank.  We want it to be in the east region for time zone reasons.  Spin one of those up from the cloud shell with the command:

    gcloud compute instances create downloader-edgar \
      --zone us-east1-b \
      --machine-type f1-micro

We're probably going to need to size the machine up to run all the downloaders...

Your environment is woefully inadequate.  To fix it do this:

    sudo apt update
    sudo apt -y upgrade
    sudo apt -y install git-all
    sudo apt -y install python3 python3-dev python3-pip
    pip3 install --upgrade google-cloud
    git clone https://github.com/benofben/arbit.git

Due to an effort from Google to make BigQuery more difficult to use than it was previously (read as "enterprise-y"), it now requires a byzantine setup to run properly.  You'll need to create a service account and do some weirdness with keys.  

First off, you need to auth gcloud by running:

    gcloud init

Now run this:

    SERVICE_ACCOUNT=downloader
    PROJECT_ID=arbit-prod
    gcloud iam service-accounts create ${SERVICE_ACCOUNT}
    gcloud projects add-iam-policy-binding ${PROJECT_ID} \
      --member "serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
      --role "roles/owner"
    gcloud iam service-accounts keys create ${SERVICE_ACCOUNT}.key.json \
      --iam-account ${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com

You're also going to need to add this to the bottom of your .profile

    export GOOGLE_APPLICATION_CREDENTIALS="downloader.key.json"

Finally, do this:

    source ~/.profile
