After the experiment has generated a dataset, we can parse and plot results with tools in this directory.

First, we have to parse from the Moongen output to an "usable format" and merge all the data that has generated from the same ruleset seed (for each ruleset seed there are five different Ruleset). Then we plot the parsed output.

* RAW DATA

a raw data example is in the directort ` $repository/RAW-DATA `:

The filename is formatted in this way: 

`acl1_1k_1_speed_21-11_01-32/MG_acl1_0.out`

`$seed_$size_speed_$experimentTimestamp/MG_$seed_$MoongenRate.out`

In each file is contained the MoonGen output from the five experiment maked with the five different ruleset of the particular seed (e.g. ACL1) at a particular rate (e.g. 0 ~= 10Gpbs)


* script_parser.sh <path to results directory>

` script_parser.sh $repository/RAW-DATA `

This script will creat a directory (elog_parsed_speed), in the path in input, in which it will be saved the new files.

E.g. all files in the directory `acl1_1k_1_speed_21-11_01-32` will be mapped in just one file `acl1_1k_tot.out`, in which each line corresponds to an experiment(same ruleset seed, same ruleset size, different ruleset, different rate), formatted in this way: `RX-pps TX-pps RX-mbit/s TX-mbit/s RX-#packets TX-#packets`


* To plot throughput we need to create a table in which are summarize raw-data (Summary directory!) and plot result from there.

