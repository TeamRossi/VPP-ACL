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
#this kind experiment will generate raw data about clock cycle spent to classify packets in fa_node.c
#it requires VALE_ELOG
#create in $EXP_RES directory a new directory called $seed_$size/ELOG_output 

#:'
for class in acl1 #acl2 acl3 acl4 acl5
do
for dirs in 1k_1 2k_1 4k_1 #8k_1 16k_1 32k_1 64k_1 
#for dirs in 1k_1 2k_1 4k_1 8k_1 16k_1 32k_1 64k_1 
do
        echo "================$dirs============="
        sh classification-time.sh $dirs $class
done
done
#'


#this kind experiment will generate raw data about ACl-ACE index matched for each packet (plus how many ht_accesses it uses) 
#in public_inlines.h
#it requires VALE_ELOG_ACL

:'
for class in acl1 acl2 acl3 acl4 acl5
do
for dirs in 1k_1 2k_1 4k_1 8k_1 16k_1 32k_1 64k_1 
do
        echo "================$dirs============="
        sh acl-matched_index.sh $dirs $class
done
mv $EXP_RES/results_$(date '+%d-%m') /Index $EXP_RES/results_$(date '+%d-%m')/Index_$(date '+%d-%m_%H-%M')
'

#vpp_compile.sh

#this kind experiment will generate MoonGen output raw data in which are recorded all RX-TX speed
#it requires NO ELOG variables activated
#create in $EXP_RES directory a new directory called $seed_$size/MG_output 
:'
for class in acl1  acl2 acl3 acl4 acl5
do
for dirs in 64k_1  #2k_1 4k_1 8k_1 16k_1 32k_1 1_1 10_1 100_1 500_1
do
        echo "================$dirs============="
        sh acl-throughput_simple.sh $dirs $class 
done
echo "=========== $(date '+%d-%m_%H-%M') ============"
done
'


echo "=========== $(date '+%d-%m_%H-%M') ============"

sudo killall vpp_main
sudo rm /tmp/cli.sock
