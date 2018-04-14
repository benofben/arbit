# setup

First off, you're going to need a local copy of this repo:

    git clone https://github.com/benofben/arbit.git
    cd arbit
    cd setup

You'll also need to install and configure the AWS CLI:

    pip install --upgrade --user awscli
    aws configure

You can make sure that the CLI is working by running:

    aws ec2 describe-regions

Next, you'll need a role to create lambdas, etc.  To create that run:

    aws iam create-role \
      --role-name arbit_role \
      --assume-role-policy-document file://arbit_role.json

You'll need to grab the role_arn from there.  Be sure to paste it at the top of 'arbit/downloader/setup.sh'
