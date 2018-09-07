mkdir trace_shot

for size in 1k 2k 4k 8k 16k 32k 64k 
do
	mkdir trace_shot/$size\_1
	path_va=trace_shot/$size\_1

	for file in $size\_1/*
	do
		##use these line to create traceset containing 10K packets
		nlines=$(wc -l $file | awk '{print $1}')
		scale=$((100000/($nlines)))
		##otherwise with scale=1 you can create traceset with number of packets equal number of rules of the ruleset
		scale=1

		echo "Ruleset size: $nlines; Scale factor: $scale"

		##Do the magic
		../VPP-ACL/ClassBench_trace_generator/trace_generator 1 1 $scale $file

		##Move traceset in the correct directory
		mv $file\_trace $path_va/
	done #file end
done #size end


