#!/bin/bash

VPPFIX=$3
echo "$VPPFIX"
dir=$1
seed=$2

dt=$(date '+%d-%m_%H-%M');
dts=$(date '+%d-%m');
echo "$dt"

for acl_rules in $RULESET/$dir/$seed*.rules;
do
rfilename="${acl_rules##/*/}"		#Ruleset filename
tfilename=$rfilename\_trace		#TraceSet filename, associated to the Ruleset
name_exp="${rfilename%\.r*}"		#Name of the experiment "acl1_seed_1"
classe_exp="${rfilename%%\_*}"		#Name of the seed "acl1"

echo "Ruleset: $acl_rules || $rfilename  || $tfilename"
echo "Classe: $classe_exp || $name_exp"


echo "VPP START DEFAULT: $VPPFIX"
sh $EXP_VPP/conf-acl.sh $VPPFIX $acl_rules
sleep 2

sh $EXP_VPP/conf-xc.sh $VPPFIX


mkdir -p $EXP_RES/results_$dts/$classe_exp\_$dir
echo "\n" > $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$name_exp.out

#for rate in 0 2500 2250 2100 2000 1900 1750 1500 1250 1000 750 500 250 100 75 50 25 15 10
for rate in 0 
do

echo "_____$rate\_____\n" 
echo "_____$rate\_____\n" >> $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$name_exp.out
echo "_____$rate\_____\n" >> $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$seed\_$rate.out

echo "MoonGen"
echo "$RULESET/trace_shot/$dir/$tfilename"
sudo $MOONGEN_PATH/build/MoonGen $MGSCR/tr_gen_timer.lua --dpdk-config=$CONFIG_DIR/dpdk-conf.lua 1 0 $RULESET/trace_shot/$dir/$tfilename -r $rate > tmp.out

cat tmp.out
cat tmp.out >> $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$name_exp.out
cat tmp.out >> $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$seed\_$rate.out
rm tmp.out

done


done
echo "mv $EXP_RES/results_$dts/$classe_exp\_$dir $EXP_RES/results_$dts/$classe_exp\_speed_$dt"
mv $EXP_RES/results_$dts/$classe_exp\_$dir $EXP_RES/results_$dts/$classe_exp\_$dir\_speed_$dt
