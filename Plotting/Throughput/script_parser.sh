#!/bin/bash

mkdir elog_parsed
echo " " > elog_parsed/acl1_$2\_tot.out
#for rate in 0 2500 2250 2100 2000 1750 1500 1250 1000 750 500 250 100 75 50 25 10 4 1;
for rate in 0 2500 2250 2100 2000 1900 1750 1500 1250 1000 750 500 250 100 75 50 25 15 10 
do

echo $1/MG_acl1_$rate.out
#python ../parserPy.py $1/MG_acl1_$rate.out parsed/acl1_$rate\_parsed.out
python parserPy.py $1/MG_acl1_$rate.out elog_parsed/tmp.out

cat elog_parsed/tmp.out >> elog_parsed/acl1_$2\_tot.out

done
