# Clear current flows
ovs-ofctl del-flows br-acl

# Add flows between port 1 (phy0) to port 2 (phy1)
ovs-ofctl add-flow br-acl table=1,priority=10,in_port=3,action=output:4
ovs-ofctl add-flow br-acl table=1,priority=11,in_port=4,action=output:3
ovs-ofctl add-flow br-acl "table=0, priority=10, actions=resubmit(,1)"

# Dump flow table
echo "sudo ovs-ofctl dump-flows br-acl"
ovs-ofctl dump-flows br-acl
