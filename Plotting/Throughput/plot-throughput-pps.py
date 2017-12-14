from matplotlib import pyplot as plt
import sys
import numbers


def loader(readfile, l_container={}): 

	l_container={'TX':[], 'RX':[]}
	cline=0
	mrx=0
	mtx=0
	for line in readfile:
	    count=0
	    for s in line.split():
                print(s +" "+str(cline))
		element = []
		if (count == 0):
			mrx = mrx + float(s)
			if cline == 4:
				mrx = mrx / 5
				element = l_container['RX']
				element.append(float(mrx))
				mrx=0
		if (count == 1):
			mtx = mtx + float(s)
			if cline == 4:
				mtx = mtx / 5
				element = l_container['TX']
				element.append(float(mtx))
				mtx=0
				cline = 0 
                        else: cline=cline + 1
		count=count+1

	readfile.close

	element = []
	element = l_container['RX']
	element.append(int(0))
	element = []
	element = l_container['TX']
	element.append(int(0))
	return l_container



try:
        print("xc: \t" + str(sys.argv[1]))
        print("a_1k: \t" + str(sys.argv[2]))
        print("a_2k: \t" + str(sys.argv[3]))
        print("a_4k: \t" + str(sys.argv[4]))
        print("a_8k: \t" + str(sys.argv[5]))

        f1 = str(sys.argv[1])
        f2 = str(sys.argv[2])
        f3 = str(sys.argv[3])
        f4 = str(sys.argv[4])
        f5 = str(sys.argv[5])

        fr1 = open(f1, 'r')
        fr2 = open(f2, 'r')
        fr3 = open(f3, 'r')
        fr4 = open(f4, 'r')
        fr5 = open(f5, 'r')
except IndexError:
        print("Error: no Filename")
        sys.exit(2)


xc_line = {}
xc_line = loader(fr1)

a1_line = {}
a1_line = loader(fr2)

a2_line = {}
a2_line = loader(fr3)

a4_line = {}
a4_line = loader(fr4)

a8_line = {}
a8_line = loader(fr5)

print(str(xc_line))
print(str(a1_line))
print(str(a4_line))


plt.style.use('valerio-slide')
#fig = plt.figure()
fig, ax = plt.subplots()


ax.plot(xc_line['TX'], xc_line['RX'],  label="X-connect")
ax.plot(a1_line['TX'], a1_line['RX'],  label="1k Ruleset-Trace")
ax.plot(a2_line['TX'], a2_line['RX'],  label="2k Ruleset-Trace")
ax.plot(a4_line['TX'], a4_line['RX'],  label="4k Ruleset-Trace")
ax.plot(a8_line['TX'], a8_line['RX'],  label="8k Ruleset-Trace")

ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dashed')

# add some text for labels, title and axes ticks
#ax.set_xlim([0,0.7])
#ax.set_ylim([0,0.7])
ax.set_xlabel('TX (Mpps)')
ax.set_ylabel('RX (Mpps)')
#ax.yaxis.set_ticks(acl_index.values())
ax.set_title('Throughput')

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])
#ax.legend([l_xc, l_a1, l_a2], ['X-connect', 'Ruleset-Trace', 'DefaultRule-trace'])


plt.savefig('pps.png')
plt.show()
