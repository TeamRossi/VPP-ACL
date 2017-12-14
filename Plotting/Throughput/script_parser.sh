#!/bin/bash
path=$1
dt=$(date '+%d-%m_%H-%M');
dts=$(date '+%d-%m');

echo "====== Parser Speed-Dataset ======="

mkdir $path/elog_parsed_speed/

for file in $path/*_speed_*/MG_*_0.out
do
tmp_class="${file%_1_speed_*}"
class="${tmp_class#$path/*}"

tmp_seed="${file#*MG_}"
seed="${tmp_seed%_0.out*}"

tmp_rate="${file#*MG_acl1_}"
rate="${tmp_rate#.out*}"

filepath="${file%MG_$seed\_*}"

echo "$file || $class || $seed"

echo "" > $path/elog_parsed_speed/$class\_tot.out


#for rate in 0 2500 2250 2100 2000 1750 1500 1250 1000 750 500 250 100 75 50 25 10 4 1;
for rate in 0 2500 2250 2100 2000 1900 1750 1500 1250 1000 750 500 250 100 75 50 25 15 10 
do

filefor=$filepath\MG_$seed\_$rate.out

#python ../parserPy.py $1/MG_acl1_$rate.out parsed/acl1_$rate\_parsed.out
python parser_speed.py $filefor $path/elog_parsed_speed/tmp.out

cat $path/elog_parsed_speed/tmp.out >> $path/elog_parsed_speed/$class\_tot.out

rm $path/elog_parsed_speed/tmp.out

done
done


echo "====== Merge Speed-Dataset (only 10Gbps) ======="
mkdir $EXP_RES/Summary/Throughput_$dt/
for file in $path/elog_parsed_speed/*_1k_tot.out
do

filename="${file#*_speed/}"
seed="${filename%_1k_*}"



echo "$file || $filename || $seed "

echo "" > $path/elog_parsed_speed/$seed\_fullspeed.out
#sed -n 2,6p $path/elog_parsed_speed/XC_tot.out > $path/elog_parsed_speed/$seed\_fullspeed.out

for size in 1 10 100 500 1k 2k 4k 8k 16k 32k
#for size in 1k 2k 4k 8k
do

sed -n 2,6p $path/elog_parsed_speed/$seed\_$size\_tot.out >> $path/elog_parsed_speed/$seed\_fullspeed.out

done

cp $path/elog_parsed_speed/$seed\_fullspeed.out $EXP_RES/Summary/Throughput_$dt/$seed\_fullspeed.out
done





