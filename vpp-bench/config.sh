#!/bin/bash

##Added by Valerio, Experiment
export EXP-VPP="VPP-ACL/Experiment"
export EXP-RES="VPP-ACL/RAW-DATA"
export RULESET="VPP-ACL/Ruleset"
export MGSCR="VPP-ACL/MoonGen_parser"

# VPP
export VPP_ROOT=vpp1704/vpp
export VPP_PLUGIN_PATH=$VPP_ROOT/build-root/install-vpp-native/vpp/lib64/vpp_api_test_plugins

# DPDK
export RTE_SDK=/usr/local/src/dpdk-17.02
export RTE_PKTGEN=/usr/local/src/pktgen-dpdk-pktgen-3.1.2
export RTE_TARGET=x86_64-native-linuxapp-gcc
# MOONGEN
export MOONGEN_PATH=/usr/local/src/MoonGen/

# Config
export CONFIG_DIR=$HOME/VPP-ACL/vpp-bench/scripts

#export PATH=$PATH:$CONFIG_DIR:$RTE_SDK/usertools
export PATH=$PATH:$CONFIG_DIR:$RTE_SDK/usertools:$VPP_ROOT/build-root/build-tool-native/tools
export C_INCLUDE_PATH=$C_INCLUDE_PATH:$VPP_ROOT/build-root/install-vpp-native/vpp/include
export STARTUP_CONF=$CONFIG_DIR/startup.conf
export DPDK_CONF=$CONFIG_DIR/tgdpdk.conf
export BINS="$VPP_ROOT/build-root/install-vpp-native/vpp/bin"
export PLUGS="$VPP_ROOT/build-root/install-vpp-native/vpp/lib64/vpp_plugins"
export SFLAG="env PATH=$PATH:$BINS"


# Aliases
#alias force-update-conf="svn export https://github.com/theleos88/vpp-bench/trunk/scripts --force $CONFIG_DIR && source $CONFIG_DIR/config.sh"
alias update-conf="source $SCRIPTS/config.sh"
alias show-conf="cat $CONFIG_DIR/config.sh"
alias list-scripts="ls -l $CONFIG_DIR/*.sh"
alias dpdk-setup="$RTE_SDK/usertools/dpdk-setup.sh"
alias vppctl="sudo $SFLAG $BINS/vppctl"
alias vppprefix="cat $STARTUP_CONF | grep prefix | cut -d'x' -f2 | xargs echo -n"
