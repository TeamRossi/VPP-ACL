#!/bin/bash

VPPFIX="vpp6637"
classe_exp=$2
dir=$1
m_name="base"

dt=$(date '+%d-%m_%H-%M');
dts=$(date '+%d-%m');
echo "$dt"


for acl_rules in $RULESET/$dir/$classe_exp*.rules;
do
rfilename="${acl_rules##/*/}"
tfilename=$rfilename\_trace
#name_exp="${rfilename%\.r*s}"
name_exp="$classe_exp""_""$dir"

echo "Ruleset: $acl_rules || $rfilename"
echo "Trace: $tfilename || $t_ext"
echo "Experiment name: $name_exp || (ext: $name_ext)"

sudo killall vpp_main
sleep 5

echo "VPP START DEFAULT: $VPPFIX"
sh $EXP_VPP/conf-acl.sh $VPPFIX $acl_rules
sleep 2

sh $EXP_VPP/conf-xc.sh $VPPFIX

cd $EXP_VPP/elog_parser/
pwd
echo "ELOG clean"
sh elog_clean.sh

mkdir -p $EXP_RES/results_$dts/Index
mkdir -p $EXP_RES/results_$dts/Index_$dts

echo "MoonGen"
echo "sudo $MOONGEN_PATH/build/MoonGen $MOONGEN_PATH/replay-pcap.lua 1 0 ~/trace/p64.pcap -l > tmp.out"
sudo $MOONGEN_PATH/build/MoonGen $MGSCR/replay-pcap.lua --dpdk-config=$CONFIG_DIR/dpdk-conf.lua 1 0 ~/trace/p64.pcap -l > tmp.out

cat tmp.out
cat tmp.out >> $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$name_exp.out
cat tmp.out >> $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$exp\_$rate.out
rm tmp.out

echo "ELOG dump"
sh elog_acl.sh

sed -n 10,20p acl_match_action
echo "mv acl_match_action $EXP_RES/results_$dts/Index/Elog_$name_exp.out"
mv acl_match_action $EXP_RES/results_$dts/Index/Elog_$name_exp.out

cd -

break

done


sudo killall vpp_main
sudo rm /tmp/cli.sock
