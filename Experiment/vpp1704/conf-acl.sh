#!/bin/bash
sudo killall vpp_main
sleep 5

echo "VPP START DEFAULT: $1"
$CONFIG_DIR/vpp_start-default.sh $1 &
sleep 20

echo "Setting Up interfaces"
sudo $SFLAG $BINS/vppctl -p $1 set int state TenGigabitEthernetb/0/1 up

sudo $SFLAG $BINS/vppctl -p $1 set int state TenGigabitEthernetb/0/0 up

echo "Setting Xconnect 1->0"
sudo $SFLAG $BINS/vppctl -p $1 set int l2 xconnect TenGigabitEthernetb/0/1 TenGigabitEthernetb/0/0



echo "Parsing ruleset: $2"
sudo $SFLAG $BINS/vppctl -p $1 acl-plugin add filename $2 permit
#sudo $SFLAG $BINS/vppctl -p $1 acl-plugin add filename /home/valerio/filters/default.rules

echo "Applying rules"
#sudo $SFLAG $BINS/vppctl -p $1 acl-plugin apply sw_if_index 2 input 0 1
sudo $SFLAG $BINS/vppctl -p $1 acl-plugin apply sw_if_index 2 input 0

#echo "ACL_VAT"
#sudo $SFLAG $BINS/vpp_api_test chroot prefix $1 plugin_path $VPP_PLUGIN_PATH in /home/valerio/vpp1704/vat-acl-script


