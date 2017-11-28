#!/bin/bash

VPPFIX="vpp1643"
dir=$1
exp=$2

dt=$(date '+%d-%m_%H-%M');
dts=$(date '+%d-%m');
echo "$dt"

for acl_rules in $RULESET/$dir/$exp*.rules;
do
rfilename="${acl_rules##/*/}"
tfilename=$rfilename\_trace
name_exp="${rfilename%\.r*}"
classe_exp="${rfilename%%\_*}"

echo "Ruleset: $acl_rules || $rfilename  || $tfilename"
echo "Classe: $classe_exp || $name_exp"

sudo killall vpp_main
sleep 5

echo "VPP START DEFAULT: $VPPFIX"
sh $VAEXP/conf-acl.sh $VPPFIX $acl_rules
sleep 2

sh $VAEXP/conf-xc.sh $VPPFIX


mkdir -p $VAEXP/results_$dts/$classe_exp\_$dir
echo "\n" > $VAEXP/results_$dts/$classe_exp\_$dir/MG_$name_exp.out

#for rate in 0 2500 2250 2100 2000 1750 1500 1250 1000 750 500 250 100 75 50 25 10 4 1;
for rate in 0 2500 2250 2100 2000 1900 1750 1500 1250 1000 750 500 250 100 75 50 25 15 10
do

echo "_____$rate\_____\n" 
echo "_____$rate\_____\n" >> $VAEXP/results_$dts/$classe_exp\_$dir/MG_$name_exp.out
echo "_____$rate\_____\n" >> $VAEXP/results_$dts/$classe_exp\_$dir/MG_$exp\_$rate.out

echo "MoonGen"
echo "$RULESET/trace_shot/$dir/$tfilename"
sudo $MOONGEN_PATH/build/MoonGen $MGSCR/tr_gen_timer.lua --dpdk-config=$CONFIG_DIR/dpdk-conf.lua 1 0 $RULESET/trace_shot/$dir/$tfilename -r $rate > tmp.out

cat tmp.out
cat tmp.out >> $VAEXP/results_$dts/$classe_exp\_$dir/MG_$name_exp.out
cat tmp.out >> $VAEXP/results_$dts/$classe_exp\_$dir/MG_$exp\_$rate.out
rm tmp.out

done


done
echo "mv $VAEXP/results_$dts/$classe_exp\_$dir $VAEXP/results_$dts/$classe_exp\_speed_$dt"
mv $VAEXP/results_$dts/$classe_exp\_$dir $VAEXP/results_$dts/$classe_exp\_$dir\_speed_$dt
