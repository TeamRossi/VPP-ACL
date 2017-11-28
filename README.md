# VPP-ACL
Initial git to share non-VPP code but useful tools for VPP-ACL related performance evaluation


# Requirement

## VPP configuration

vpp-bench: leo's link

Requirement:

* config.source
* vpp_start-default.sh

vpp-acl_plugin: we have introduced a function in order to parse the Ruleset file and create an ACL; and we have introduced two different Elog structure in order to capture Classification Time and matched ACE_Index

## Moongen

moongen:

## Classbench

Internet service providers are reluctant to distribute copies of real filter sets for security and confidentiality reasons, hence realistic test vectors are a scarce commodity. The small subset of the research community who obtain real filter sets either limit performance evaluation to the small sample space or employ ad hoc methods of modifying those filter sets. 
The Filter Set Generator produces synthetic filter sets that accurately model the characteristics of real filter sets. 
The Trace Generator that produces a sequence of packet headers to exercise the synthetic filter set. 
Classbench link: (https://www.arl.wustl.edu/classbench/)

### Ruleset

Partition sort paper (http://ieeexplore.ieee.org/abstract/document/7784429/)

### Classbench trace generator



## Plotting

**Requirement: Matplotlib Python2**

To install Matplotlib at the system-level, we recommend that you use your distribution’s package manager. This will guarantee that Matplotlib’s dependencies will be installed as well.

If, for some reason, you cannot use the package manager, you may use the wheels available on PyPI:

python -mpip install matplotlib