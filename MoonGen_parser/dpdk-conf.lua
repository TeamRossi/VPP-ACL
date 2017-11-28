-- Configuration for all DPDK command line parameters.
-- See DPDK documentation at http://dpdk.org/doc/guides/testpmd_app_ug/run_app.html for details.
-- libmoon tries to choose reasonable defaults, so this config file can almost always be empty.
-- Be careful when running libmoon in a VM that also uses another virtio NIC, e.g., for internet access.
-- In this case it may be necessary to use the blacklist or whitelist features in some configurations.
DPDKConfig {
	-- configure the CPU cores to use, default: all cores
	-- cores = {0, 15, 16,18,19},
	cores = {0, 37, 38,39,40},
	
	-- max number of shared tasks running on core 0
	--sharedCores = 8,

	-- black or whitelist devices to limit which PCI devs are used by DPDK
	-- only one of the following examples can be used

	--pciWhitelist = {"LC1P0",      "LC1P1"},
	pciWhitelist = {"0000:84:00.0", "0000:84:00.1"},
	
	-- arbitrary DPDK command line options
	-- the following configuration allows multiple DPDK instances (use together with pciWhitelist)
	-- cf. http://dpdk.org/doc/guides/prog_guide/multi_proc_support.html#running-multiple-independent-dpdk-applications
	cli = {
		"--file-prefix", "m1",
		"--socket-mem", "16384,16384"
	}

}
