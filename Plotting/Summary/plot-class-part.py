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
					element = l_container['us']
					element.append(float(s))
				if cline == 3:
					element = l_container['clock']
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
	
	#x_raw=[1, 2, 10, 100, 500, 1000, 2000, 4000, 8000]
	x_raw=[2, 10, 100, 500, 1000, 2000, 4000, 8000, 16000, 32000]
	x=[float(math.log(elem, 2.0)) for elem in x_raw]
	min_x=min(x)
	max_x=max(x)
	print(str(x))
	y=seed_line
	print(str(seed_line))
	#del y[0]

	#f_interpol = interp1d(x, y, kind='cubic') 
	f_interpol = interp1d(x, y, kind='linear') 

	xnew = np.linspace(min_x, max_x, num=36, endpoint=True)
	seed_interpol = f_interpol(xnew)
	
		
	exp=float(35.0/(max_x))
	x_exp= [elem*exp for elem in x]
	print(str(exp) +" " + str(x_exp) +" " + str(len(seed_line)))

	return seed_interpol,xnew,x


try:
        print("file1: \t" + str(sys.argv[1]))
        print("file2: \t" + str(sys.argv[2]))
        print("file3: \t" + str(sys.argv[3]))
        print("file4: \t" + str(sys.argv[4]))
        print("file5: \t" + str(sys.argv[5]))

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
seed1a, x1a, xxa = seed_interpol(seed1_line['us'])
seed1b, x1b, xxb = seed_interpol(seed1_line['part'])

seed2_line = {}
seed2_line = loader(fr2)
seed2a, x2a, xxa = seed_interpol(seed2_line['us'])
seed2b, x2b, xxb = seed_interpol(seed2_line['part'])

seed3_line = {}
seed3_line = loader(fr3)
seed3a, x3a, xxa = seed_interpol(seed3_line['us'])
seed3b, x3b, xxb = seed_interpol(seed3_line['part'])

seed4_line = {}
seed4_line = loader(fr4)
seed4a, x4a, xxa = seed_interpol(seed4_line['us'])
seed4b, x4b, xxb = seed_interpol(seed4_line['part'])

seed5_line = {}
seed5_line = loader(fr5)
seed5a, x5a, xxa = seed_interpol(seed5_line['us'])
seed5b, x5b, xxb = seed_interpol(seed5_line['part'])


print(str(seed1a))
print(str(seed1_line))



plt.style.use('valerio-slide')
#fig = plt.figure()
fig1, ax = plt.subplots(figsize=(14, 8))
ax.set_title('VPP 17.10 - TM - Classification Time (@10Gbps)')

ax.plot(x1a, seed1a, '--', label='ACL_1')
ax.plot(x2a, seed2a, '--', label='ACL_2')
ax.plot(x3a, seed3a, '--', label='ACL_3')
ax.plot(x4a, seed4a, '--', label='ACL_4')
ax.plot(x5a, seed5a, '--', label='ACL_5')

ax.set_ylabel(u'${\mu}s$')
ax.set_xlabel('Ruleset size')
ax.set_xticks(xxa)
ax.set_xticklabels(['1','10','100','500','1K','2K','4K','8K','16K','32K'])

ax.set_axisbelow(True)
ax.xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
ax.yaxis.grid(color='gray', linestyle='dashed', linewidth=1)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])

fig2, ax2 = plt.subplots(figsize=(14, 8))
ax2.set_title('VPP 17.10 - TM')

ax2.plot(x1b, seed1b, '--', label='ACL_1')
ax2.plot(x2b, seed2b, '--', label='ACL_2')
ax2.plot(x3b, seed3b, '--', label='ACL_3')
ax2.plot(x4b, seed4b, '--', label='ACL_4')
ax2.plot(x5b, seed5b, '--', label='ACL_5')

ax2.set_ylabel('Partition (Count.)')
ax2.set_xlabel('Ruleset size')
ax2.set_xticks(xxb)
ax2.set_xticklabels(['1','10','100','500','1K','2K','4K','8K','16K','32K'])

ax2.set_axisbelow(True)
ax2.xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
ax2.yaxis.grid(color='gray', linestyle='dashed', linewidth=1)


handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles[::-1], labels[::-1])


fig1.savefig('pps1.png')
fig2.savefig('pps2.png')
#plt.show()

