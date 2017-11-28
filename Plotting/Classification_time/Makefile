path=./

a_1k=elog_parsed/Elog_acl1_1k_tot.out
a_2k=elog_parsed/Elog_acl1_2k_tot.out
a_4k=elog_parsed/Elog_acl1_4k_tot.out
a_8k=elog_parsed/Elog_acl1_8k_tot.out

dt=$(shell date '+%d-%m_%H-%M')

boxplot:
	python boxplot_1M.py $(path)/$(a_1k) $(path)/$(a_2k) $(path)/$(a_4k) $(path)/$(a_8k) 
	mv boxplot.png bp_$(shell date '+%d-%m_%H-%M').png

hist:
	python hist_avg_1M.py  $(path)/$(a_1k) $(path)/$(a_2k) $(path)/$(a_4k) $(path)/$(a_8k) 
	mv hist_1m.png hist_$(shell date '+%d-%m_%H-%M').png

