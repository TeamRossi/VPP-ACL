from matplotlib import pyplot as plt
import sys

def loader(readfile, l_container={}): 

	l_container={'diff':[],'speed':[],'TX':[], 'RX':[]}
	cline=0
	mrx=0
	mtx=0
	msx=0
	for line in readfile:
	    count=0
	    for s in line.split():
		element = []
		if count == 1:
			msx = msx + float(s)
			if cline > 4:
				msx = msx / 5
				element = l_container['speed']
				element.append(float(msx))
				msx=0
		if count == 4:
			mrx = mrx + int(s)
			if cline > 4:
				mrx = mrx / 5
				element = l_container['RX']
				element.append(int(mrx))
				mrx=0
		if count == 5:
			mtx = mtx + int(s)
			if cline > 4:
				mtx = mtx / 5
				element = l_container['TX']
				element.append(int(mtx))
				mtx=0
				cline = 0 
		count=count+1
	    cline=cline + 1

	readfile.close

	element = []
	element = l_container['speed']
	element.append(int(0))
	element = []
	element = l_container['RX']
	element.append(int(0))
	element = []
	element = l_container['TX']
	element.append(int(0))

	elem=0
	while elem < len(l_container['speed']):
		element=[]
		element = l_container['diff']
		if l_container['TX'][elem] != 0:
			diff = (l_container['TX'][elem] - l_container['RX'][elem])*100/l_container['TX'][elem]
		else: diff=0
		print(diff)
		element.append(int(diff))
		elem=elem+1

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

#fig = plt.figure()
fig, ax = plt.subplots()

ax.plot(xc_line['speed'], xc_line['diff'], label="X-connect")
ax.plot(a1_line['speed'], a1_line['diff'], label="1k Ruleset-Trace")
ax.plot(a2_line['speed'], a2_line['diff'], label="2k Ruleset-Trace")
ax.plot(a4_line['speed'], a4_line['diff'], label="4k Ruleset-Trace")
ax.plot(a8_line['speed'], a8_line['diff'], label="8k Ruleset-Trace")

ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dashed')

# add some text for labels, title and axes ticks
ax.set_xlim([0,0.3])
ax.set_ylim([0,0.1])
ax.set_xlabel('TX (Mpps)')
ax.set_ylabel('Drop Rate (%)')
#ax.yaxis.set_ticks(acl_index.values())
ax.set_title('Throughput')

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])


plt.savefig('pkts.png')
plt.show()
