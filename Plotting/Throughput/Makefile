path=./

xc_f=$(path)/elog_parsed_speed/XC_1k_tot.out
a_1k=$(path)/elog_parsed_speed/acl1_1k_tot.out
a_2k=$(path)/elog_parsed_speed/acl1_2k_tot.out
a_4k=$(path)/elog_parsed_speed/acl1_4k_tot.out
a_8k=$(path)/elog_parsed_speed/acl1_8k_tot.out

dt=$(shell date '+%d-%m_%H-%M')

plot_mbit:
	python plot-throughput-mbit.py $(xc_f) $(a_1k) $(a_2k) $(a_4k) $(a_8k) 
	mv mbit.png $(path)/mbit-$(dt).png

plot_pps:
	python plot-throughput-pps.py $(xc_f) $(a_1k) $(a_2k) $(a_4k) $(a_8k) 
	mv pps.png $(path)/pps-$(dt).png

plot_diff:
	python plot-throughput-pkts.py $(xc_f) $(a_1k) $(a_2k) $(a_4k) $(a_8k) 
	mv pkts.png $(path)/pkts-$(dt).png

