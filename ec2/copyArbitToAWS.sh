#!/bin/sh
IP=54.173.70.188

cd /home/ben/arbitWorkspace
tar cf - arbit | gzip -c > /home/ben/ec2/arbit.tgz
cd -

ssh -i ./arbit.pem ec2-user@$IP rm -rf arbit
scp -i ./arbit.pem -r /home/ben/ec2/arbit.tgz ec2-user@$IP:~
ssh -i ./arbit.pem ec2-user@$IP tar -xvf /home/ec2-user/arbit.tgz
