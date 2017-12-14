#!/bin/bash

VPPFIX="vpp3653"
dir=$1
seed=$2

dt=$(date '+%d-%m_%H-%M');
dts=$(date '+%d-%m');
echo "$dt"

for acl_rules in $RULESET/$dir/$seed*.rules;
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
sh $EXP_VPP/conf-acl.sh $VPPFIX $acl_rules
sleep 2

sh $EXP_VPP/conf-xc.sh $VPPFIX

cd $EXP_VPP/elog_parser
pwd

echo "ELOG clean"
sh elog_clean.sh

mkdir -p $EXP_RES/results_$dts/$classe_exp\_$dir
echo "\n" > $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$name_exp.out

echo "MoonGen"
echo "sudo $MOONGEN_PATH/build/MoonGen $MGSCR/tr_gen_timer.lua --dpdk-config=$CONFIG_DIR/dpdk-conf.lua 1 0 $RULESET/trace_shot/$dir/$tfilename > tmp.out"
sudo $MOONGEN_PATH/build/MoonGen $MGSCR/tr_gen_timer.lua --dpdk-config=$CONFIG_DIR/dpdk-conf.lua 1 0 $RULESET/trace_shot/$dir/$tfilename > tmp.out

cat tmp.out
cat tmp.out >> $EXP_RES/results_$dts/$classe_exp\_$dir/MG_$name_exp.out
rm tmp.out

echo "ELOG dump"
sh elog_clk.sh

sed -n 10,20p clk_output_elog
cat clk_output_elog > $EXP_RES/results_$dts/$classe_exp\_$dir/Elog_$name_exp.out
cat clk_output_elog >> $EXP_RES/results_$dts/$classe_exp\_$dir/Elog_$seed.out
rm clk_output_elog 
#mv clk_output_elog $EXP_RES/results/$classe_exp/Elog_$name_exp.out

cd -
pwd

done

echo "mv $EXP_RES/results_$dts/$classe_exp\_$dir $EXP_RES/results_$dts/$classe_exp\_clk_$dt"
mv $EXP_RES/results_$dts/$classe_exp\_$dir $EXP_RES/results_$dts/$classe_exp\_$dir\_clk_$dt
