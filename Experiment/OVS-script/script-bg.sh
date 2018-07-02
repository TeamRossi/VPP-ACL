#Set CPU in performance mode
sudo cpupower frequency-set -g performance

sleep 2
#Deactivate turbo boost!
echo 1 | sudo tee  /sys/devices/system/cpu/intel_pstate/no_turbo

sleep 2

#Cleaning?
echo 60 | sudo tee /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages
sudo rm /dev/hugepages/*

sleep 2
#================================================================

:'
#for class in acl1 acl2 acl3 acl4 acl5
for class in fw1 fw2 fw3 fw4 fw5 ipc1 ipc2
do
for dirs in 64k_1 #
#for dirs in 1k_1 2k_1 4k_1 8k_1 16k_1 32k_1 64k_1
do
	echo "================$dirs============="
	sh acl-throughput_caida.sh $dirs $class 
done
echo 60 | sudo tee /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages
sudo rm /dev/hugepages/*

sleep 2
done
'

echo "=========== $(date '+%d-%m_%H-%M') ============"


#:'
for class in fw1 fw2 fw3 fw4 fw5 ipc1 ipc2
do
#for dirs in 1_1 10_1 100_1 500_1 1k_1 2k_1 4k_1 8k_1 16k_1 32k_1 64k_1 #
for dirs in 64k_1 #
do
	echo "================$dirs============="
	sh acl-throughput_cb.sh $dirs $class 
done
echo 60 | sudo tee /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages
sudo rm /dev/hugepages/*

sleep 2
done
#'

echo "=========== $(date '+%d-%m_%H-%M') ============"

