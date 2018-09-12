#!/bin/bash

#dir=$1
#exp=$2
dir=1k_1
exp=acl1

dt=$(date '+%d-%m_%H-%M');
dts=$(date '+%d-%m');
echo "$dt"

for acl_rules in $RULESET/$dir/$exp*.rules;
do
rfilename="${acl_rules##/*/}"
tfilename=$rfilename\_trace
name_exp="${rfilename%\.r*}"
#classe_exp="${rfilename%%\_*}"
classe_exp="XC"

echo "Ruleset: $acl_rules || $rfilename  || $tfilename"
echo "Classe: $classe_exp || $name_exp"

sudo killall vpp_main
sleep 5

echo "VPP START DEFAULT"
$CONFIG_DIR/vpp_start-default.sh &
sleep 25

sh $EXP_VPP/conf-xc.sh 


mkdir -p $EXP_RES/results_$dts/$classe_exp\_$dir
echo "\n" > $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$name_exp.out

#for rate in 0 2500 2250 2100 2000 1900 1750 1500 1250 1000 750 500 250 100 75 50 25 15 10
for rate in 0 
do


echo "_____$rate\_____\n" 
echo "_____$rate\_____\n" >> $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$name_exp.out 
echo "_____$rate\_____\n" >> $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$exp\_$rate.out

echo "MoonGen"
echo "sudo $MOONGEN_PATH/build/MoonGen $MOONGEN_PATH/replay-pcap.lua 1 0 ~/trace/p64.pcap -l > tmp.out"
sudo $MOONGEN_PATH/build/MoonGen $MGSCR/replay-pcap.lua --dpdk-config=$CONFIG_DIR/dpdk-conf.lua 1 0 ~/trace/p64.pcap -l > tmp.out

cat tmp.out
cat tmp.out >> $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$name_exp.out 
cat tmp.out >> $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$exp\_$rate.out
rm tmp.out

done


done

echo "mv $EXP_RES/results_$dts/$classe_exp\_$dir $EXP_RES/results_$dts/$classe_exp\_speed_$dt"
mv $EXP_RES/results_$dts/$classe_exp\_$dir $EXP_RES/results_$dts/$classe_exp\_$dir\_speed_$dt




sudo killall vpp_main
sudo rm /tmp/cli.sock
