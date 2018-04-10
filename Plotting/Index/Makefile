path=./Pictures
dt=$(shell date '+%d-%m_%H-%M')


hist_maskid:
	python parser_seed.py file_info/script-maskid.info file_info/single-index.info
	mv pps1.png $(path)/hist_maskid_$(shell date '+%d-%m_%H-%M').png

hist_access:
	python parser_seed.py file_info/script-accesses.info file_info/single-index.info
	mv pps1.png $(path)/hist_access_$(shell date '+%d-%m_%H-%M').png



comp_acc:
	python general-6.py file_info/script-access-index.info file_info/compare-access.info
	mv pps1.png $(path)/comp_access-$(dt).png
	mv pps2.png $(path)/comp_lookup-$(dt).png
