After the experiment has generated a dataset, we can parse and plot results with tools in this directory.

First, we have to merge all the data that has generated from the same ruleset seed (for each ruleset seed there are five different Ruleset). Then we plot the parsed output.

* RAW_DATA

a raw data example is in the directort ` $repository/RAW-DATA `

The filename is formatted in this way:

`acl1_1k_1_clk_22-11_12-04/Elog_acl1_seed_1.out`

`$seed_$size_clk_$experimentTimestamp/Elog_$seed_seed_$#experiment.out`

In each file is contained the Elog events (struct{$vector_size \t $clock_cycles}) for the experiment with that particular ruleset

* script_merge_exp.sh <raw data directory>

` script_merge_exp $repository/RAW-DATA `

This script will create a directory (elog_parsed_clk), in the path put in input, in which it will be saved the new files.

E.g. all files in the directory `acl1_1k_1_clk_22-11_12-04/` will be mapped in just one file `Elog_acl1_1k_tot.out`, in which each column corresponds to an experiment(same ruleset seed, same ruleset size, different ruleset), in which each element corresponds to the classification time average in clock cycles (clock_cycle/vector_size)

* make hist path=<$elog_parsed_speed>

`hist`: to plot the histogram of classification time distributions per ruleset size.

It needs 4 files in input that it will take from the path in input (you can modify file from variables in the Makefile)

```
a_1k=$(path)/elog_parsed_clk/Elog_acl1_1k_tot.out
a_2k=$(path)/elog_parsed_clk/Elog_acl1_2k_tot.out
a_4k=$(path)/elog_parsed_clk/Elog_acl1_4k_tot.out
a_8k=$(path)/elog_parsed_clk/Elog_acl1_8k_tot.out
```


