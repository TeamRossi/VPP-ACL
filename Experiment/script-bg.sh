:'
for dirs in 2k_1 4k_1 8k_1 1k_1
do
	echo "================$dirs============="
	sh acl-throughput.sh $dirs acl1
done
'

:'
for exp in acl3 acl4 acl5
do
for dirs in 8k_1
do
	echo "================$dirs============="
	sh classification-time.sh $dirs $exp
done
done
'



for dirs in 1_1 10_1 100_1 500_1
do
	echo "================$dirs============="
	sh acl-throughput.sh $dirs acl1 
done


:'
for dirs in 1_1 10_1 100_1 500_1
do
	echo "================$dirs============="
	sh classification-time.sh $dirs acl1
done
'
