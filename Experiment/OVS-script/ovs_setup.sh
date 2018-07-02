# reboot ovs
export PATH=$PATH:/usr/local/share/openvswitch/scripts
export DB_SOCK=/usr/local/var/run/openvswitch/db.sock

ovs-ctl stop
ovs-ctl --no-ovs-vswitchd start

ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-init=true
ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-socket-mem="1024,0"
ovs-ctl --no-ovsdb-server --db-sock="$DB_SOCK" start


#create bridge
ovs-vsctl add-br br-acl -- set bridge br-acl datapath_type=netdev

#export LC0P0/LC0P1 (NUMA node 0)
ovs-vsctl add-port br-acl dpdk-lc0p0 -- set Interface dpdk-lc0p0 type=dpdk \
    options:dpdk-devargs=0000:0b:00.0
ovs-vsctl add-port br-acl dpdk-lc0p1 -- set Interface dpdk-lc0p1 type=dpdk \
    options:dpdk-devargs=0000:0b:00.1

return

#export LC1P0/LC1P1 (NUMA node 1)
ovs-vsctl add-port br-acl dpdk-lc1p0 -- set Interface dpdk-lc1p0 type=dpdk \
    options:dpdk-devargs=0000:84:00.0
ovs-vsctl add-port br-acl dpdk-lc1p1 -- set Interface dpdk-lc1p1 type=dpdk \
    options:dpdk-devargs=0000:84:00.1
