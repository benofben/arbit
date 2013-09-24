#!/bin/sh

# since we're using dhcp, the ips change all the time
echo "" > ~/.ssh/known_hosts

sshpass -p root ssh -o StrictHostKeyChecking=no root@10.0.0.251 reboot
sshpass -p root ssh -o StrictHostKeyChecking=no root@10.0.0.252 reboot
sshpass -p root ssh -o StrictHostKeyChecking=no root@10.0.0.253 reboot
sshpass -p root ssh -o StrictHostKeyChecking=no root@10.0.0.254 reboot

