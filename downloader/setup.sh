#!/usr/bin/env bash

# This script assumes a configured AWS CLI.
# (1) Create lambda functions for the downloader
# (2) Download old data
# (3) Setup jobs to download new nightly data

aws create-function \
--function-name edgar \
--runtime python3.6 \
--role <value> \
--handler <value>
