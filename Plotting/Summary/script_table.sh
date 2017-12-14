path=$EXP_RES/Summary/
dt=$(date '+%d-%m_%H-%M');
dts=$(date '+%d-%m');


mkdir $EXP_RES/Summary/Table_$dt/
mkdir $EXP_RES/Summary/tmp

for seed in acl1 acl2 acl3 acl4 acl5
do

echo "====$seed===="
echo $seed >> $path/Table_$dt/Total.out 

throughput_file=$path/*/$seed\_fullspeed.out
if touch $throughput_file ; then
    echo "Command succeeded"
else
    echo "Command failed"
    touch $EXP_RES/Summary/tmp/$seed\_fullspeed.out
fi

classification_file=$path/*/$seed\_classification.out 
if touch $classification_file ; then
    echo "Command succeeded"
else
    echo "Command failed"
    touch $EXP_RES/Summary/tmp/$seed\_classification.out
fi

partition_file=$path/*/$seed\_partition.out
if touch $partition_file ; then
    echo "Command succeeded"
else
    echo "Command failed"
    touch $EXP_RES/Summary/tmp/$seed\_partition.out
fi

summary_file=$path/Table_$dt/$seed\_table.out

touch $throughput_file $classification_file $partition_file $summary_file
python parser_table.py $throughput_file $classification_file $partition_file $summary_file

cat $summary_file
cat $summary_file >> $path/Table_$dt/Total.out 


rm -rf $EXP_RES/Summary/tmp

done
