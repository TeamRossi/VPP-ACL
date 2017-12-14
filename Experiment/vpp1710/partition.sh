VPPFIX="vpp8654"
dir=$1
seed=$2

dt=$(date '+%d-%m_%H-%M');
dts=$(date '+%d-%m');
echo "$dt"


mkdir -p $EXP_RES/Summary/Partition_$dts/

echo "______$dir\__$seed____" 
echo "______$dir\__$seed____" >> $EXP_RES/Summary/Partition_$dts/$seed\_partition.out

for exp in 1 2 3 4 5
do

for acl_rules in $RULESET/$dir/$seed\_seed_$exp.rules;
do
rfilename="${acl_rules##/*/}"		#Ruleset filename
tfilename=$rfilename\_trace		#TraceSet filename, associated to the Ruleset
name_exp="${rfilename%\.r*}"		#Name of the experiment "acl1_seed_1"
classe_exp="${rfilename%%\_*}"		#Name of the seed "acl1"

echo "Ruleset: $acl_rules || $rfilename  || $tfilename"
echo "Classe: $classe_exp || $name_exp"

sudo killall vpp_main
sleep 5

echo "VPP START DEFAULT: $VPPFIX"
sh $EXP_VPP/conf-acl.sh $VPPFIX $acl_rules
sleep 2

#sh $EXP_VPP/conf-xc.sh $VPPFIX

sudo -E $BINS/vppctl -s /tmp/cli.sock acl-plugin show partition sw_if_index 2 input 0 > tmp.out
#sudo -E $BINS/vppctl -s /tmp/cli.sock acl-plugin show partition sw_if_index 2 input 0 verbose > tmp.out

cat tmp.out
cat tmp.out >> $EXP_RES/Summary/Partition_$dts/$seed\_partition.out
rm tmp.out

done
done
