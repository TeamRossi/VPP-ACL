path=$1
dt=$(date '+%d-%m_%H-%M');
dts=$(date '+%d-%m');

rm -rf $path/elog_parsed_clk/

echo "=======MergePerExp========="
mkdir $path/elog_parsed_clk/
mkdir $EXP_RES/Summary/Classification_$dt/

for size in 1 10 100 500 1k 2k 4k 8k 16k 32k 64k
do
for file in $path/*_$size\_1_clk_*/Elog_*_seed_1.out
do
tmp_class="${file%_1_clk_*}"
class="${tmp_class#$path/*}"
seed="${class%_*}"
filepath="${file%_seed_*}"

echo "$file || $class || $filepath"


echo "python parser_seed.py $filepath\_seed_1.out $filepath\_seed_2.out $filepath\_seed_3.out $filepath\_seed_4.out $filepath\_seed_5.out $path/elog_parsed_clk/Elog_$class\_tot.out tmp.out"

python parser_seed.py $filepath\_seed_1.out $filepath\_seed_2.out $filepath\_seed_3.out $filepath\_seed_4.out $filepath\_seed_5.out $path/elog_parsed_clk/Elog_$class\_tot.out tmp.out

cat tmp.out
cat tmp.out >> $path/elog_parsed_clk/$seed\_classification.out
cat tmp.out >> $EXP_RES/Summary/Classification_$dt/$seed\_classification.out

rm tmp.out

done
done
