pathp=$(HOME)/Table_Summary/Pictures_S/hist

dt=$(shell date '+%d-%m_%H-%M')

hist_tss_us:
	python hist_general.py file_info/script-us_tss.info file_info/vpp1710_tss.info
	mv hist.png $(pathp)/hist_tss_us_$(shell date '+%d-%m_%H-%M').png
	mv hist.pdf $(pathp)/hist_tss_us_$(shell date '+%d-%m_%H-%M').pdf
	mv hist.svg $(pathp)/hist_tss_us_$(shell date '+%d-%m_%H-%M').svg

hist_tm_us:
	python hist_general.py file_info/script-us_tm.info file_info/vpp1710_tm.info
	mv hist.png $(pathp)/hist_tm_us_$(shell date '+%d-%m_%H-%M').png
	mv hist.pdf $(pathp)/hist_tm_us_$(shell date '+%d-%m_%H-%M').pdf
	mv hist.svg $(pathp)/hist_tm_us_$(shell date '+%d-%m_%H-%M').svg

hist_ls_us:
	python hist_general.py file_info/script-us_ls.info file_info/vpp1704_ls.info
	mv hist.png $(pathp)/hist_ls_us_$(shell date '+%d-%m_%H-%M').png
	mv hist.pdf $(pathp)/hist_ls_us_$(shell date '+%d-%m_%H-%M').pdf
	mv hist.svg $(pathp)/hist_ls_us_$(shell date '+%d-%m_%H-%M').svg
