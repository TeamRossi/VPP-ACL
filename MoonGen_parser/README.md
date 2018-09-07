# MoonGen scripts to send ClassBench traces

In order to run MoonGen you have to write the following command:
` sudo $MOONGEN_PATH/build/MoonGen $MOONGEN_SCRIPT --dpdk-config=dpdk-conf.lua`

In our scenario we developed three script to do different things with the traffic generator:
1. `tr_gen_shot.lua`: It takes in input a ClassBench traceset and send it in one shot at full speed. 

`` sudo $MOONGEN_PATH/build/MoonGen tr_gen_shot.lua --dpdk-config=/dpdk-conf.lua $TX-PORT $RX-PORT $TRACESET -r $RATE  ``

2. `tr_gen_timer.lua`: It takes in input a ClassBench traceset and send it in loop for 25 seconds at full speed. 

`` sudo $MOONGEN_PATH/build/MoonGen tr_gen_timer.lua --dpdk-config=/dpdk-conf.lua $TX-PORT $RX-PORT $TRACESET -r $RATE  ``


3. `replay-pcap.lua`: It is the official script to send pcap on the interface. (we used this script in order to test ACL with real traffic from CAIDA)

`` sudo $MOONGEN_PATH/build/MoonGen replay-pcap.lua --dpdk-config=/dpdk-conf.lua $TX-PORT $RX-PORT $PCAP_FILE -l ``



-------

In `verbose` directory you can find a script that use the original function to collect statistics from the devices. In previous scripts I modified how they show these statistics in output in order to be parsed by scripts in the Plotting section

