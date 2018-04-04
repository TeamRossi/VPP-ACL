#Deactivate turbo boost!
echo 1 | sudo tee  /sys/devices/system/cpu/intel_pstate/no_turbo
#================================================================

#sh xc-throughput.sh 

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

#:'
count=$((123))
for class in  acl1 acl2 acl3 acl4 acl5
do
#for dirs in 1_1 10_1 100_1 500_1 1k_1 2k_1 4k_1 8k_1 16k_1
for dirs in 64k_1
do
	count=$(($count + 1))

	sudo killall vpp_main
	sudo kill -9 $(ps -aux | grep vpp | awk '{print $2}')

	echo 60 | sudo tee /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages
	sudo rm /dev/hugepages/*
	sleep 2

	echo "================$dirs============="
	sh classification-time.sh $dirs $class "vpp$count"
done
done
#'

vpp_compile.sh

#:'
count=$((101))
for class in acl1 acl2 acl3 acl4 acl5
do
#for dirs in 1_1 10_1 100_1 500_1 1k_1 2k_1 4k_1 8k_1 16k_1 32k_1
for dirs in 64k_1 
do
	count=$(($count + 1))
	sudo killall vpp_main
	sudo kill -9 $(ps -aux | grep vpp | awk '{print $2}')
	echo 60 | sudo tee /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages
	sudo rm /dev/hugepages/*
	sleep 2

	echo "================$dirs============="
	sh acl-throughput_simple.sh $dirs $class "vpp$count"
done
done
#'


echo "=========== $(date '+%d-%m_%H-%M') ============"



sudo killall vpp_main
sudo rm /tmp/cli.sock
