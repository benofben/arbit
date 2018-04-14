# downloader

First off, you're going to need a local copy of this repo:

    git clone https://github.com/benofben/arbit.git
    cd arbit

You'll also need to install and configure the AWS CLI:

    pip install --upgrade --user awscli
    aws configure

Next, you'll need a role to create lambdas, etc.  To create that run:

    aws iam create-role \
      --role-name basic_lambda_role \
      --assume-role-policy-document file://basic_lambda_role.json

You'll need to grab the role_arn from there and add it to 'setup.sh'.

With all that in place, you'll want to set up the downloader by running:

    cd downloader
    ./setup.sh
