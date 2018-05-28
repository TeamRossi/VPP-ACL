pathp=$(HOME)/Table_Summary/Pictures_S

dt=$(shell date '+%d-%m_%H-%M')

comp_vpp:
	python general-11.py file_info/script-thr-part.info file_info/compare-vpps.info
	mv pps1.png $(pathp)/png/comp_vpp_throughput-$(dt).png
	mv pps1.pdf $(pathp)/pdf/comp_vpp_throughput-$(dt).pdf
	mv pps1.svg $(pathp)/svg/comp_vpp_throughput-$(dt).svg
	mv pps2.png $(pathp)/png/comp_vpp_partition-$(dt).png
	mv pps2.pdf $(pathp)/pdf/comp_vpp_partition-$(dt).pdf
	mv pps2.svg $(pathp)/svg/comp_vpp_partition-$(dt).svg


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
	python general-11.py file_info/script-class-part.info file_info/compare-tot.info
	mv pps1.png $(pathp)/png/comp_tot_classification-$(dt).png
	mv pps1.pdf $(pathp)/pdf/comp_tot_classification-$(dt).pdf
	mv pps1.svg $(pathp)/svg/comp_tot_classification-$(dt).svg
	mv pps2.png $(pathp)/png/comp_tot_partition_log-$(dt).png
	mv pps2.pdf $(pathp)/pdf/comp_tot_partition_log-$(dt).pdf
	mv pps2.svg $(pathp)/svg/comp_tot_partition_log-$(dt).svg




tm_seed:
	python general-11.py file_info/script-thr-part.info file_info/tm_seeds.info
	mv pps1.png $(pathp)/png/tm_seed_throughput-$(dt).png
	mv pps1.pdf $(pathp)/pdf/tm_seed_throughput-$(dt).pdf
	mv pps1.svg $(pathp)/svg/tm_seed_throughput-$(dt).svg
	mv pps2.png $(pathp)/png/tm_seed_partition-$(dt).png
	mv pps2.pdf $(pathp)/pdf/tm_seed_partition-$(dt).pdf
	mv pps2.svg $(pathp)/svg/tm_seed_partition-$(dt).svg

tm_seed2:
	python general-11.py file_info/script-class-part.info file_info/tm_seeds.info
	mv pps1.png $(pathp)/tm_seed_classification-$(dt).png
	mv pps2.png $(pathp)/tm_seed_partition-$(dt).png

tm_seed_off:
	python general-11.py file_info/script-class-part.info file_info/tm_off_seeds.info
	mv pps1.png $(pathp)/tm_seed_off_classification-$(dt).png
	mv pps2.png $(pathp)/tm_seed_off_partition-$(dt).png

vpp10_seed:
	python general-11.py file_info/script-thr-part.info file_info/vpp1710_seeds.info
	mv pps1.png $(pathp)/vpp1710_seed_throughput-$(dt).png
	mv pps2.png $(pathp)/vpp1710_seed_partition-$(dt).png

vpp10_seed2:
	python general-11.py file_info/script-class-part.info file_info/vpp1710_seeds.info
	mv pps1.png $(pathp)/vpp1710_seed_classification-$(dt).png
	mv pps2.png $(pathp)/vpp1710_seed_partition-$(dt).png

vpp04_seed:
	python general-11.py file_info/script-class-part.info file_info/vpp1704_seeds.info
	mv pps1.png $(pathp)/vpp1704_seed_classification-$(dt).png
	mv pps2.png $(pathp)/vpp1704_seed_partition-$(dt).png

vpp04_seed2:
	python general-11.py file_info/script-thr-part.info file_info/vpp1704_seeds.info
	mv pps1.png $(pathp)/vpp1704_seed_throughput-$(dt).png
	mv pps2.png $(pathp)/vpp1704_seed_partition-$(dt).png




scatter:
	python plot-scatter.py file_info/script-scatter.info file_info/scatter.info
	mv pps1.png $(pathp)/png/scatter-$(dt).png
	mv pps1.pdf $(pathp)/pdf/scatter-$(dt).pdf
	mv pps1.svg $(pathp)/svg/scatter-$(dt).svg
