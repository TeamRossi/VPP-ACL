path=$1
dt=$(date '+%d-%m_%H-%M');
dts=$(date '+%d-%m');

rm -rf $path/elog_parsed_index/

echo "=======MergePerExp========="
mkdir $path/elog_parsed_index/
mkdir $EXP_RES/Summary/Index_$dt/

for size in 1k 2k 4k 8k 16k 32k
do
for file in $path/Elog_*_$size\_1.out
do
tmp_class="${file##/*/}"
class="${tmp_class#Elog_*}"
seed="${class%%_*.out}"
filepath="${file%_seed_*}"

echo "$file || $seed || $filepath"

touch tmp.out
echo "python parser_seed.py $file tmp.out"
python parser_seed.py $file tmp.out

cat tmp.out
cat tmp.out >> $path/elog_parsed_index/$seed\_index.out
cat tmp.out >> $EXP_RES/Summary/Index_$dt/$seed\_index.out

rm tmp.out

done
done


echo "========Create table============="

for file in $EXP_RES/Summary/Index_$dt/*_index.out
do

echo "python parser_table.py $file tmp.out"
python parser_table.py $file tmp.out

cat tmp.out
cat tmp.out > $file
rm tmp.out

done


for seed in acl1 acl2 acl3 acl4 acl5
do

echo "$seed" >> $EXP_RES/Summary/Index_$dt/Total_index.out
cat $EXP_RES/Summary/Index_$dt/$seed\_index.out >> $EXP_RES/Summary/Index_$dt/Total_index.out

done
