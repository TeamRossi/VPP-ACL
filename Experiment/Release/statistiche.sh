
#number of entries per partition
sudo -E $BINS/vppctl -s /tmp/cli.sock acl-plugin show collisions sw_if_index 2 input 0 | awk '{print $4}' | sort | uniq -c

#number of collisions per entry
sudo -E $BINS/vppctl -s /tmp/cli.sock acl-plugin show collisions sw_if_index 2 input 0 | awk '{print $5}' | sort | uniq -c

#list of partion
sudo -E $BINS/vppctl -s /tmp/cli.sock acl-plugin show partition sw_if_index 2 input 0 verbose | grep type

