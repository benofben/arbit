#!/bin/sh

mkdir /arbitnfs
mkdir /arbit

mount 10.0.0.1:/srv/nfs/arbit /arbitnfs
cp /arbitnfs/*.py /arbit
cd /arbit
python client.py > out1.txt &
python client.py > out2.txt &
python client.py > out3.txt &
python client.py > out4.txt &
