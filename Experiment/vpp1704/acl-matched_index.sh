#!/bin/bash

VPPFIX="vpp6637"
classe_exp="acl1"
classe_ext="acl2"
m_name="base"

dt=$(date '+%d-%m_%H-%M');
echo "$dt"


for acl_rules in $RULESET/1k_1/$classe_exp*.rules;
do
rfilename="${acl_rules##/*/}"
tfilename=$rfilename\_trace
name_exp="${rfilename%\.r*s}"
name_ext=$classe_ext"${name_exp##*$classe_exp}"
t_ext=$name_ext.rules_trace

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

mkdir $EXP_RES/results/$classe_exp

echo "MoonGen"
sudo $MOONGEN_PATH/build/MoonGen $MGSCR/tr_gen_shot.lua --dpdk-config=$CONFIG_DIR/dpdk-conf.lua 1 0 $RULESET/trace_shot/1k_1/$tfilename > $EXP_RES/results/$classe_exp/MG_$name_exp.out

echo "ELOG dump"
sh elog_acl.sh

mv acl_match_action $EXP_RES/results/$classe_exp/Elog_$name_exp.out

echo "ELOG clean"
sh elog_clean.sh

echo "MoonGen"
sudo $MOONGEN_PATH/build/MoonGen $MGSCR/tr_gen_shot.lua --dpdk-config=$CONFIG_DIR/dpdk-conf.lua 1 0 $RULESET/trace_shot/1k_1/$t_ext > $EXP_RES/results/$classe_exp/MG_$name_ext.out

echo "ELOG dump"
sh elog_acl.sh

mv acl_match_action $EXP_RES/results/$classe_exp/Elog_$name_ext.out


cd -

break

done
echo "mv $EXP_RES/results/$classe_exp $EXP_RES/results/$classe_exp\_index_$dt"
mv $EXP_RES/results/$classe_exp $EXP_RES/results/$classe_exp\_index_$dt
