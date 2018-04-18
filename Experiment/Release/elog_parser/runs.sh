#!/bin/bash

source $CONFIG_DIR/config.sh
PREFIX=`cat $STARTUP_CONF | grep prefix | awk '{print $2}' | xargs echo -n`

#sudo $SFLAG $BINS/vppctl -p $PREFIX $1
sudo -E $BINS/vppctl -s /tmp/cli.sock $@
