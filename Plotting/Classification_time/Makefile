path=./
seed="acl1"

a_1k=$(path)/elog_parsed_clk/Elog_$(seed)_1k_tot.out
a_2k=$(path)/elog_parsed_clk/Elog_$(seed)_2k_tot.out
a_4k=$(path)/elog_parsed_clk/Elog_$(seed)_4k_tot.out
a_8k=$(path)/elog_parsed_clk/Elog_$(seed)_8k_tot.out

dt=$(shell date '+%d-%m_%H-%M')

boxplot_clock:
	python boxplot_cc.py  $(a_1k) $(a_2k) $(a_4k) $(a_8k)
	mv boxplot.png $(path)/bp_cc_$(shell date '+%d-%m_%H-%M').png

boxplot_us:
	python boxplot_us.py  $(a_1k) $(a_2k) $(a_4k) $(a_8k)
	mv boxplot.png $(path)/bp_us_$(shell date '+%d-%m_%H-%M').png

hist_clock:
	python hist_cc.py  $(a_1k) $(a_2k) $(a_4k) $(a_8k) 
	mv hist_1m.png $(path)/hist_cc_$(shell date '+%d-%m_%H-%M').png

hist_us:
	python hist_us.py  $(a_1k) $(a_2k) $(a_4k) $(a_8k) 
	mv hist_1m.png $(path)/hist_us_$(shell date '+%d-%m_%H-%M').png

