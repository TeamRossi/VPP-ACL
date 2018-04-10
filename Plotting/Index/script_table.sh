path=$1


rm -rf $path/Paths_*.out
rm -rf $path/Tot_table.out

for seed in acl1 acl2 acl3 acl4 acl5
do

touch $path/Elog_$seed\_table.out

for size in 1k 2k 4k 8k 16k 32k 64k
do

echo "$path/Elog_${seed}_${size}_1.out,vpp" >> $path/Paths_$seed.out

done

python parser_table.py $path/Paths_$seed.out $path/Elog_$seed\_table.out

echo $seed >> $path/Tot_table.out
cat $path/Elog_$seed\_table.out >> $path/Tot_table.out

done
