cd $Ruleset/norange
pwd

for size in 1_1 10_1 100_1 500_1 1k_1 2k_1 4k_1 8k_1 16k_1 32k_1 64k_1
do
mkdir -p ovs/$size/
done



for file in *_1/*.rules
do

file_out="ovs/${file}"
echo "$file - $file_out"

cat $file | awk -F '@' '{print $2}' | awk 'BEGIN{count=65530;} {count=count-1; proto="tcp"; if ($9=="0x01/0xFF"){proto="icmp"}else if ($9=="0x11/0xFF"){proto="udp"}else{proto="tcp"} printf("table=0,priority=%d,ip,nw_src=%s,nw_dst=%s,%s,tp_src=%s,tp_dst=%s,actions=resubmit(,1) \n", count, $1, $2, proto, $3, $6)}' > $file_out

done
return

file=$1
fileout=$file"_ovs"

cat $file | awk -F '@' '{print $2}' | awk 'BEGIN{count=65530;} {count=count-1; proto="tcp"; if ($9=="0x01/0xFF"){proto="icmp"}else if ($9=="0x11/0xFF"){proto="udp"}else{proto="tcp"} printf("table=0,priority=%d,ip,nw_src=%s,nw_dst=%s,%s,tp_src=%s,tp_dst=%s,actions=resubmit(,1) \n", count, $1, $2, proto, $3, $6)}' > $fileout
