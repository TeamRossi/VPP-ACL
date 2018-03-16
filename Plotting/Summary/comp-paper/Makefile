path=$(EXP_RES)/Summary
pathp=$(EXP_RES)/Pictures

s1=$(path)/acl1_table.out
s2=$(path)/acl2_table.out
s3=$(path)/acl3_table.out
s4=$(path)/acl4_table.out
s5=$(path)/acl5_table.out

dt=$(shell date '+%d-%m_%H-%M')

plot_sum:
	python plot-throughput.py $(s1) $(s2) $(s3) $(s4) $(s5) 
	mv pps.png $(pathp)/sum_throughput-$(dt).png

plot_class_part:
	python plot-class-part.py $(s1) $(s2) $(s3) $(s4) $(s5) 
	mv pps1.png $(pathp)/sum_class-$(dt).png
	mv pps2.png $(pathp)/sum_part-$(dt).png

pathv1=/home/valerio/vpp1704/Results/Summary/
pathv2=/home/valerio/vpp1710/Results/Summary/
st1=$(pathv1)/Total.out
stnr1=$(pathv2)/norange/Table_12-12_11-16/Total.out
st2=$(pathv2)/Total.out

comp_vpp:
	python comp-vpp-version.py $(st1) $(st2)
	mv pps1.png $(pathp)/comp_vpp_throughput-$(dt).png
	mv pps2.png $(pathp)/comp_vpp_partition-$(dt).png

comp_norange:
	python comp-norange.py $(stnr1) $(st2)
	mv pps1.png $(pathp)/comp_nr_throughput-$(dt).png
	mv pps2.png $(pathp)/comp_nr_partition-$(dt).png

