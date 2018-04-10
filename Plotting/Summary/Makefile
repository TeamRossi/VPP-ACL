pathp=Pictures

dt=$(shell date '+%d-%m_%H-%M')

comp_vpp:
	python general-11.py file_info/script-thr-part.info file_info/compare-vpps.info
	mv pps1.png $(pathp)/comp_vpp_throughput-$(dt).png
	mv pps2.png $(pathp)/comp_vpp_partition-$(dt).png

comp_vpp2:
	python general-11.py file_info/script-class-part.info file_info/compare-vpps.info
	mv pps1.png $(pathp)/comp_vpp_classification-$(dt).png
	mv pps2.png $(pathp)/comp_vpp_partition-$(dt).png

comp_paper:
	python general-11.py file_info/script-class-part.info file_info/compare-papers.info
	mv pps1.png $(pathp)/comp_paper_classification-$(dt).png
	mv pps2.png $(pathp)/comp_paper_partition_log-$(dt).png

comp_tm:
	python general-11.py file_info/script-class-part.info file_info/compare-tm.info
	mv pps1.png $(pathp)/comp_tm_classification-$(dt).png
	mv pps2.png $(pathp)/comp_tm_partition_log-$(dt).png

comp_tot:
	python general-11.py file_info/script-class-part.info file_info/compare-tot1.info
	mv pps1.png $(pathp)/comp_tot_classification-$(dt).png
	mv pps2.png $(pathp)/comp_tot_partition_log-$(dt).png




tm_seed:
	python general-11.py file_info/script-thr-part.info file_info/tm_seeds.info
	mv pps1.png $(pathp)/tm_seed_throughput-$(dt).png
	mv pps2.png $(pathp)/tm_seed_partition-$(dt).png

tm_seed2:
	python general-11.py file_info/script-class-part.info file_info/tm_seeds.info
	mv pps1.png $(pathp)/tm_seed_classification-$(dt).png
	mv pps2.png $(pathp)/tm_seed_partition-$(dt).png

tm_seed_off:
	python general-11.py file_info/script-class-part.info file_info/tm_off_seeds.info
	mv pps1.png $(pathp)/tm_seed_off_classification-$(dt).png
	mv pps2.png $(pathp)/tm_seed_off_partition-$(dt).png
