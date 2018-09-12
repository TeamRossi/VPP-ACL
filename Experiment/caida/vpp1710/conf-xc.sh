#!/bin/bash


echo "Setting Up interfaces"
sudo -E $BINS/vppctl -s /tmp/cli.sock set int state TenGigabitEthernetb/0/1 up
sudo -E $BINS/vppctl -s /tmp/cli.sock set int state TenGigabitEthernetb/0/0 up

echo "Setting Xconnect 0->1"
sudo -E $BINS/vppctl -s /tmp/cli.sock set int l2 xconnect TenGigabitEthernetb/0/1 TenGigabitEthernetb/0/0
echo "Setting Xconnect 1->0"
sudo -E $BINS/vppctl -s /tmp/cli.sock set int l2 xconnect TenGigabitEthernetb/0/0 TenGigabitEthernetb/0/1


