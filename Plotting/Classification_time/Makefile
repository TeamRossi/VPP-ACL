path=./

a_1k=$(path)/elog_parsed_clk/Elog_acl1_1k_tot.out
a_2k=$(path)/elog_parsed_clk/Elog_acl1_2k_tot.out
a_4k=$(path)/elog_parsed_clk/Elog_acl1_4k_tot.out
a_8k=$(path)/elog_parsed_clk/Elog_acl1_8k_tot.out

dt=$(shell date '+%d-%m_%H-%M')

boxplot:
	python boxplot_1M.py  $(a_1k) $(a_2k) $(a_4k) $(a_8k)
	mv boxplot.png $(path)/bp_$(shell date '+%d-%m_%H-%M').png

hist:
	python hist_avg_1M.py  $(a_1k) $(a_2k) $(a_4k) $(a_8k) 
	mv hist_1m.png $(path)/hist_$(shell date '+%d-%m_%H-%M').png

