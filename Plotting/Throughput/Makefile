path=./

xc_f=elog_parsed/acl1_xc_tot.out
a_1k=elog_parsed/acl1_1k_tot.out
a_2k=elog_parsed/acl1_2k_tot.out
a_4k=elog_parsed/acl1_4k_tot.out
a_8k=elog_parsed/acl1_8k_tot.out

dt=$(shell date '+%d-%m_%H-%M')

plot_mbit:
	python plot-throughput-mbit.py $(path)/$(a_1k) $(path)/$(a_2k) $(path)/$(a_4k) $(path)/$(a_8k)
	mv mbit.png mbit-$(dt).png

plot_pps:
	python plot-throughput-pps.py $(path)/$(a_1k) $(path)/$(a_2k) $(path)/$(a_4k) $(path)/$(a_8k)
	mv pps.png pps-$(dt).png

plot_diff:
	python plot-throughput-pkts.py $(path)/$(a_1k) $(path)/$(a_2k) $(path)/$(a_4k) $(path)/$(a_8k)
	mv pkts.png pkts-$(dt).png
