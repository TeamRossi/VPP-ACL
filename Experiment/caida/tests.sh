#!/bin/bash
sudo -E $BINS/vppctl -s /tmp/cli.sock acl-plugin add filename /home/valerio/Ruleset/8k_1/acl4_seed_1.rules
sudo -E $BINS/vppctl -s /tmp/cli.sock acl-plugin add filename /home/valerio/Ruleset/16k_1/acl3_seed_1.rules
sudo -E $BINS/vppctl -s /tmp/cli.sock acl-plugin add filename /home/valerio/Ruleset/1k_1/acl3_seed_1.rules

echo "Applying rules"
#sudo -E $BINS/vppctl -s /tmp/cli.sockacl-plugin apply sw_if_index 2 input 0 1
sudo -E $BINS/vppctl -s /tmp/cli.sock acl-plugin apply sw_if_index 2 input 0 1

sudo -E $BINS/vppctl -s /tmp/cli.sock acl-plugin show partition sw_if_index 2 input 0

echo "sudo -E \$BINS/vppctl -s /tmp/cli.sock acl-plugin show partition sw_if_index 2 input 0"
#echo "ACL_VAT"
#sudo $SFLAG $BINS/vpp_api_test chroot prefix $1 plugin_path $VPP_PLUGIN_PATH in /home/valerio/vpp1704/vat-acl-script


