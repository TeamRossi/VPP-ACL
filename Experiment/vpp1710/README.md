Ruleset path format: `VPP-ACL/Ruleset/1k_1/acl1_seed_1.rules` (`VPP-ACL/Ruleset/$directory/$seed\_seed_X.rules`)

E.g. `$directory = VPP-ACL/Ruleset/1k_1` and `$seed = acl1`


`sh acl-throughput.sh $directory $seed`

`sh classification-time.sh $directory $seed`
 
 
 
**Requirement:**

We use [vpp-bench](https://github.com/theleos88/vpp-bench) to start and configure VPP. And we also need, as you can see from `VPP-ACL/vpp-bench/`, a new set of variables:
```
export EXP-VPP="VPP-ACL/Experiment"
export EXP-RES="VPP-ACL/RAW-DATA"
export RULESET="VPP-ACL/Ruleset"
export MGSCR="VPP-ACL/MoonGen_parser"
```
