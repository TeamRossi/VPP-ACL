
echo "=======MergePerExp========="

mkdir $1/elog_parsed
for file in $1/*_clk_*/Elog_*.out
do
class="${file%_1_clk_*}"
filepath="${file%_seed_*}"

echo "$file || $class || $filepath"
python parser_seed.py $filepath\_seed_1.out $filepath\_seed_2.out $filepath\_seed_3.out $filepath\_seed_4.out $filepath\_seed_5.out $1/elog_parsed/Elog_$class\_tot.out

done

