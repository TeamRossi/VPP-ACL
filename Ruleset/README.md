### Ruleset (from PartitionSort)

We use the ClassBench utility to generate rulesets since we do not have access to real rulesets. These rulesets are designed to mimic real rulesets. It includes 12 parameter files that are divided into three different categories: 5 access control lists (ACL), 5 firewalls (FW) and 2 IP chains (IPC). We generate lists of 1K, 2K, 4K, 8K, 16K, 32K, and 64K rules. For each size, we generate 5 classifiers for each parameter file, yielding 60 classifiers per size and 420 classifiers total.

[Yingchareonthawornchai, S., Daly, J., Liu, A. X., & Torng, E. (2016, November). A sorted partitioning approach to high-speed and fast-update OpenFlow classification. In Network Protocols (ICNP), 2016 IEEE 24th International Conference on (pp. 1-10). IEEE.](http://ieeexplore.ieee.org/abstract/document/7784429/)


You can find also an archive in which there are modified rulesets (used to test OVS) where port ranges are transformed in exact matches: 

` norange.tar.xz  `

---

### Classbench trace generator

In order to evaluate the throughput of techniques employing caching or the power consumption of various devices under load, we must exercise the algorithm or device using a sequence of synthetic packet headers. The Trace Generator produces a list of synthetic packet headers that probe filters in a given filter set. Note that we do not want to generate random packet headers. Rather, we want to ensure that a packet header is covered by at least one filter in the FilterSet in order to exercise the packet classifier and avoid default filter matches. 

*Use this tool to generate traces to exercise these rulesets.*

[Taylor, D. E., & Turner, J. S. (2007). Classbench: A packet classification benchmark. IEEE/ACM Transactions on Networking (TON), 15(3), 499-511.](https://dl.acm.org/citation.cfm?id=1295239)

#### An easy way to generate a Traceset

I made a script that automate the generation of 'trace_shot'(traceset that has uniform distribution in the rules that match) from original rulesets:

` sh generate_trace.sh `
