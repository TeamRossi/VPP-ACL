from matplotlib import pyplot as plt
import sys
import math
import numbers
import numpy as np

from scipy.interpolate import interp1d

def loader(readfile, l_container={}): 

	l_container={'size':[], 'thr':[], 'clock':[], 'us':[], 'part':[]}
	cline=0
	count=0
	for line in readfile:
		for s in line.split():
			element = []
			if count > 0 :
				if cline == 0:
					element = l_container['size']
					element.append(s)
				if cline == 1:
					element = l_container['thr']
					element.append(float(s))
				if cline == 2:
					element = l_container['clock']
					element.append(float(s))
				if cline == 3:
					element = l_container['us']
					element.append(float(s))
				if cline == 4:
					element = l_container['part']
					element.append(int(s))
			else: count = 1
		cline=cline + 1
		count=0

	readfile.close

	return l_container

def seed_interpol(seed_line):
	seed_interpol=[]
	
	#x_raw=[2, 10, 100, 500, 1000, 2000, 4000, 8000]
	x_raw=[2, 10, 100, 500, 1000, 2000, 4000, 8000, 16000, 32000]
	x=[float(math.log(elem, 2.0)) for elem in x_raw]
	min_x=min(x)
	max_x=max(x)
	print(str(x))
	y=seed_line['thr']
	print(str(seed_line))
	#del y[0]

	#f_interpol = interp1d(x, y, kind='cubic') 
	f_interpol = interp1d(x, y, kind='linear') 

	xnew = np.linspace(min_x, max_x, num=36, endpoint=True)
	seed_interpol = f_interpol(xnew)
	
		
	exp=float(35.0/(max_x))
	x_exp= [elem*exp for elem in x]
	print(str(exp) +" " + str(x_exp) +" " + str(len(seed_line['thr'])))

	return seed_interpol,xnew,x


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


seed1_line = {}
seed1_line = loader(fr1)
seed1, x1, xx = seed_interpol(seed1_line)

seed2_line = {}
seed2_line = loader(fr2)
seed2, x2, xx = seed_interpol(seed2_line)

seed3_line = {}
seed3_line = loader(fr3)
seed3, x3, xx = seed_interpol(seed3_line)

seed4_line = {}
seed4_line = loader(fr4)
seed4, x4, xx = seed_interpol(seed4_line)

seed5_line = {}
seed5_line = loader(fr5)
seed5, x5, xx = seed_interpol(seed5_line)


print(str(seed1))
print(str(seed1_line))


plt.style.use('valerio-slide')
#fig = plt.figure()
fig, ax = plt.subplots(figsize=(14,8))

ax.plot(x1, seed1, '--', label='ACL_1')
ax.plot(x2, seed2, '--', label='ACL_2')
ax.plot(x3, seed3, '--', label='ACL_3')
ax.plot(x4, seed4, '--', label='ACL_4')
ax.plot(x5, seed5, '--', label='ACL_5')

plt.xticks(xx,['1','10','100','500','1K','2K','4K','8K','16K','32K'])
#plt.yticks(line)
#plt.yscale('log')

#ax.xaxis.set_ticks(np.arange(start, end, stepsize))

ax.set_axisbelow(True)
ax.xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
ax.yaxis.grid(color='gray', linestyle='dashed', linewidth=1)

# add some text for labels, title and axes ticks
ax.set_ylim([0,6.5])
#ax.set_ylim([0,1])
ax.set_xlabel('Ruleset size')
ax.set_ylabel('RX (Mpps)')
#ax.yaxis.set_ticks(acl_index.values())
ax.set_title('Throughput @10Gbps')
#ax.set_title('VPP 17.04 - Throughput @10Gbps')
#ax.set_title('VPP 17.10 - Throughput @10Gbps')

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])


plt.savefig('pps.png')
plt.show()

