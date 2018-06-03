# arbit/downloader

## Setup

In an effort to make BigQuery more difficult to use than it was previously, BigQuery now requires a byzantine setup to run properly.  You'll need to create a service account and do some weirdness with keys.

In a cloud shell run this:

    SERVICE_ACCOUNT=downloader
    PROJECT_ID=arbit-prod
    gcloud iam service-accounts create downloader
    gcloud projects add-iam-policy-binding ${PROJECT_ID} \
      --member "serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
      --role "roles/owner"
    gcloud iam service-accounts keys create key.json \
      --iam-account ${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com

You'll need to copy that key file to every machine running a downloader component and then run:

    export GOOGLE_APPLICATION_CREDENTIALS="key.json"
