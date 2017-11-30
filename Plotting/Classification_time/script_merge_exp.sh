path=$1


echo "=======MergePerExp========="
mkdir $path/elog_parsed_clk/

for file in $path/*_clk_*/Elog_*.out
do
tmp_class="${file%_1_clk_*}"
class="${tmp_class#$path/*}"
filepath="${file%_seed_*}"

echo "$file || $class || $filepath"


echo "python parser_seed.py $filepath\_seed_1.out $filepath\_seed_2.out $filepath\_seed_3.out $filepath\_seed_4.out $filepath\_seed_5.out $path/elog_parsed_clk/Elog_$class\_tot.out"

python parser_seed.py $filepath\_seed_1.out $filepath\_seed_2.out $filepath\_seed_3.out $filepath\_seed_4.out $filepath\_seed_5.out $path/elog_parsed_clk/Elog_$class\_tot.out

done

