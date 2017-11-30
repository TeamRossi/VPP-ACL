#!/bin/bash
path=$1

echo "====== Parser Speed-Dataset ======="

mkdir $path/elog_parsed_speed/

for file in $path/*_speed_*/MG_acl1_0.out
do
tmp_class="${file%_1_speed_*}"
class="${tmp_class#$path/*}"

tmp_rate="${file#*MG_acl1_}"
rate="${tmp_rate#.out*}"

filepath="${file%MG_acl1_*}"

echo "$file || $class || $rate"

echo " " > $path/elog_parsed_speed/$class\_tot.out


#for rate in 0 2500 2250 2100 2000 1750 1500 1250 1000 750 500 250 100 75 50 25 10 4 1;
for rate in 0 2500 2250 2100 2000 1900 1750 1500 1250 1000 750 500 250 100 75 50 25 15 10 
do

filefor=$filepath\MG_acl1_$rate.out

#python ../parserPy.py $1/MG_acl1_$rate.out parsed/acl1_$rate\_parsed.out
python parser_speed.py $filefor $path/elog_parsed_speed/tmp.out

cat $path/elog_parsed_speed/tmp.out >> $path/elog_parsed_speed/$class\_tot.out

done
done