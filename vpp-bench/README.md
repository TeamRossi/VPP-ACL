It is important to setup the system to modify this variable based on your configuration in your system! (`config.sh`)

## VPP-ACL repository
```
##Added by Valerio, Experiment
export EXP-VPP="VPP-ACL/Experiment"
export EXP-RES="VPP-ACL/RAW-DATA"
export RULESET="VPP-ACL/Ruleset"
export MGSCR="VPP-ACL/MoonGen_parser"
```

```
# Config
export CONFIG_DIR=$HOME/VPP-ACL/vpp-bench/scripts
```

---
## VPP
```
export VPP_ROOT=vpp1704/vpp
```


## Packet generation module

### DPDK
```
export RTE_SDK=/usr/local/src/dpdk-17.02
export RTE_PKTGEN=/usr/local/src/pktgen-dpdk-pktgen-3.1.2
export RTE_TARGET=x86_64-native-linuxapp-gcc
```

### MOONGEN
```
export MOONGEN_PATH=/usr/local/src/MoonGen/
```

at the end export these variables in the system `source config.sh`

---
---

# VPP startup

In the startup.conf is stored information used by VPP to configure the framework, take a look to [their documentation: detailed list of options for startup-conf file](https://wiki.fd.io/view/VPP/Command-line_Arguments)
