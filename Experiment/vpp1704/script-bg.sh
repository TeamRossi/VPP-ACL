#Deactivate turbo boost!
echo 1 | sudo tee  /sys/devices/system/cpu/intel_pstate/no_turbo
#================================================================

sh xc-throughput.sh 

:'
for class in acl1
do
for dirs in 2k_1 4k_1 8k_1 1k_1
do
	echo "================$dirs============="
	sh acl-throughput.sh $dirs $class
done
done
'

:'
for class in acl3 acl4 acl5
do
for dirs in 8k_1
do
	echo "================$dirs============="
	sh classification-time.sh $dirs $class
done
done
'

for class in acl1
do
for dirs in 16k_1 32k_1 
do
	echo "================$dirs============="
	sh acl-throughput_simple.sh $dirs $class 
done
done


echo "=========== $(date '+%d-%m_%H-%M') ============"



sudo killall vpp_main
sudo rm /tmp/cli.sock
