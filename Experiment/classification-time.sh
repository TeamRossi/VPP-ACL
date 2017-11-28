#!/bin/bash

VPPFIX="vpp2653"
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

sh $VAEXP/xc.sh $VPPFIX

cd $VAEXP/elog_parser
pwd

echo "ELOG clean"
sh elog_clean.sh

mkdir -p $VAEXP/results_$dts/$classe_exp\_$dir
echo "\n" > $VAEXP/results_$dts/$classe_exp\_$dir/MG_$name_exp.out

echo "MoonGen"
echo "sudo $MOONGEN_PATH/build/MoonGen $MGSCR/tr_gen_timer.lua --dpdk-config=$CONFIG_DIR/dpdk-conf.lua 1 0 $RULESET/trace_shot/$dir/$tfilename > tmp.out"
sudo $MOONGEN_PATH/build/MoonGen $MGSCR/tr_gen_timer.lua --dpdk-config=$CONFIG_DIR/dpdk-conf.lua 1 0 $RULESET/trace_shot/$dir/$tfilename > tmp.out

cat tmp.out
cat tmp.out >> $VAEXP/results_$dts/$classe_exp\_$dir/MG_$name_exp.out
rm tmp.out

echo "ELOG dump"
sh elog_clk.sh

sed -n 10,20p clk_output_elog
cat clk_output_elog > $VAEXP/results_$dts/$classe_exp\_$dir/Elog_$name_exp.out
cat clk_output_elog >> $VAEXP/results_$dts/$classe_exp\_$dir/Elog_$exp.out
rm clk_output_elog 
#mv clk_output_elog $VAEXP/results/$classe_exp/Elog_$name_exp.out

cd -
pwd

done

echo "mv $VAEXP/results_$dts/$classe_exp\_$dir $VAEXP/results_$dts/$classe_exp\_clk_$dt"
mv $VAEXP/results_$dts/$classe_exp\_$dir $VAEXP/results_$dts/$classe_exp\_$dir\_clk_$dt
