from matplotlib import pyplot as plt
import sys
import math
import numbers
import numpy as np

from scipy.interpolate import interp1d

def loaderPaper(readfile, l_container={}): 

	l_container={'size':[], 'class':[], 'part':[], 'cons':[], 'quer':[]}
	cline=-1
	count=0
	firstime=0
	for line in readfile:
		for s in line.split():
			element = []
			if count > 0 :
				if ((firstime) == 0) :
					if cline == 0:
						element = l_container['size']
						element.append(s)
					if cline == 1:
						element = l_container['class']
						element.append(float(s))
					if cline == 2:
						element = l_container['part']
						element.append(float(s))
					if cline == 3:
						element = l_container['cons']
						element.append(float(s))
					if cline == 4:
						element = l_container['quer']
						element.append(float(s))
				else :
					if cline == 1:
						element = l_container['class'][(count-1)]
						element = element +float(s)
						l_container['class'][(count-1)] = element
					if cline == 2:
						element = l_container['part'][(count-1)]
						element = element +float(s)
						l_container['part'][(count-1)] = element
					if cline == 3:
						element = l_container['cons'][(count-1)]
						element = element +float(s)
						l_container['cons'][(count-1)] = element
					if cline == 4:
						element = l_container['quer'][(count-1)]
						element = element +float(s)
						l_container['quer'][(count-1)] = element
				count = count + 1
			else: count = count + 1
		cline=cline + 1
		count=0
		if cline > 4: 
		   	cline=-1
			firstime = firstime + 1

	readfile.close

	for column in range(len(l_container['size'])):
		element = l_container['class'][(column-1)]
		element = element/firstime
		l_container['class'][(column-1)] = element
		element = l_container['part'][(column-1)]
		element = element/firstime
		l_container['part'][(column-1)] = element
		element = l_container['cons'][(column-1)]
		element = element/firstime
		l_container['cons'][(column-1)] = element
		element = l_container['quer'][(column-1)]
		element = element/firstime
		l_container['quer'][(column-1)] = element

	return l_container

def loaderVpp(readfile, l_container={}): 

	l_container={'size':[], 'thr':[], 'clock':[], 'us':[], 'part':[]}
	cline=-1
	count=0
	firstime=0
	for line in readfile:
		for s in line.split():
			element = []
			if count > 0 :
				if ((firstime) == 0) :
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
						element.append(float(s))
				else :
					if cline == 1:
						element = l_container['thr'][(count-1)]
						element = element +float(s)
						l_container['thr'][(count-1)] = element
					if cline == 2:
						element = l_container['clock'][(count-1)]
						element = element +float(s)
						l_container['clock'][(count-1)] = element
					if cline == 3:
						element = l_container['us'][(count-1)]
						element = element +float(s)
						l_container['us'][(count-1)] = element
					if cline == 4:
						element = l_container['part'][(count-1)]
						element = element +float(s)
						l_container['part'][(count-1)] = element
				count = count + 1
			else: count = count + 1
		cline=cline + 1
		count=0
		if cline > 4: 
		   	cline=-1
			firstime = firstime + 1

	readfile.close

	for column in range(len(l_container['size'])):
		#element = l_container['thr'][(column-1)]
		#element = element/firstime
		#l_container['thr'][(column-1)] = element
		element = l_container['clock'][(column-1)]
		element = element/firstime
		l_container['clock'][(column-1)] = element
		element = l_container['us'][(column-1)]
		element = element/firstime
		l_container['us'][(column-1)] = element
		element = l_container['part'][(column-1)]
		element = element/firstime
		l_container['part'][(column-1)] = element

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
	print("gnu_active: \t" + str(sys.argv[5]))

        f1 = str(sys.argv[1])
        f2 = str(sys.argv[2])
        f3 = str(sys.argv[3])
        f4 = str(sys.argv[4])
        gnu_active = int(sys.argv[5])

        fr1 = open(f1, 'r')
        fr2 = open(f2, 'r')
        fr3 = open(f3, 'r')
        fr4 = open(f4, 'r')
except IndexError:
        print("Error: no Filename")
        sys.exit(2)


seed1_line = {}
seed1_line = loaderPaper(fr1)
seed1a = np.average(seed1_line['cons'])
seed1b = np.average(seed1_line['class'])
area1 = [np.std(seed1_line['class']), np.std(seed1_line['cons'])]
print("TSS: "+str(seed1a)+"-"+str(seed1b))

seed2_line = {}
seed2_line = loaderPaper(fr2)
seed2a = np.average(seed2_line['cons'])
seed2b = np.average(seed2_line['class'])
area2 = [np.std(seed2_line['class']), np.std(seed2_line['cons'])]
print("TM: "+str(seed2a)+"-"+str(seed2b))

seed3_line = {}
seed3_line = loaderPaper(fr3)
seed3a = np.average(seed3_line['cons'])
seed3b = np.average(seed3_line['class'])
area3 = [np.std(seed3_line['class']), np.std(seed3_line['cons'])]
print("PS: "+str(seed3a)+"-"+str(seed3b))

seed4_line = {}
seed4_line = loaderPaper(fr4)
seed4a = np.average(seed4_line['cons'])
seed4b = np.average(seed4_line['class'])
area4 = [np.std(seed4_line['class']), np.std(seed4_line['cons'])]

print("SS: "+str(seed4a)+"-"+str(seed4b))
#print("SS: "+str(seed4_line['cons'])+str(seed4_line['class']))


plt.style.use('valerio-slide')
#fig = plt.figure()


fig1, (ax1, ax2) = plt.subplots(2,1, figsize=(14, 8), sharex=True)

area = np.pi*185
ax1.scatter(seed1b, seed1a, s=area, alpha=0.75, label='Tuple Space Search')
ax1.scatter(seed2b, seed2a, s=area, alpha=0.75, label='TupleMerge')
ax1.scatter(seed3b, seed3a, s=area, alpha=0.75, label='PartitionSort')
ax1.scatter(seed4b, seed4a, s=area, alpha=0.75, label='SmartSplit')

ax2.scatter(seed1b, seed1a, s=area, alpha=0.75, label='Tuple Space Search')
ax2.scatter(seed2b, seed2a, s=area, alpha=0.75, label='TupleMerge')
ax2.scatter(seed3b, seed3a, s=area, alpha=0.75, label='PartitionSort')
ax2.scatter(seed4b, seed4a, s=area, alpha=0.75, label='SmartSplit')


ax1.set_xticks(np.arange(0,3,0.10))
ax2.set_xticks(np.arange(0,3,0.10))

ax1.set_ylabel('Update Time ' + u'$(ms)$', labelpad=20)
ax1.yaxis.set_label_coords(1.05, -0.025)
ax2.set_xlabel('Classification Time ' + u'$({\mu}s)$')

ax1.set_axisbelow(True)
ax1.xaxis.grid(color='gray', linestyle='dashed', linewidth=1)
ax1.yaxis.grid(color='gray', linestyle='dashed', linewidth=1)
ax2.set_axisbelow(True)
ax2.xaxis.grid(color='gray', linestyle='dashed', linewidth=1)
ax2.yaxis.grid(color='gray', linestyle='dashed', linewidth=1)


handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[::-1], labels[::-1])

# zoom-in / limit the view to different portions of the data
ax1.set_ylim(3800, 4100)  # outliers only
ax2.set_ylim(0, 20)  # most of the data

# hide the spines between ax and ax2
ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.xaxis.tick_top()
ax1.tick_params(labeltop='off')  # don't put tick labels at the top
ax2.xaxis.tick_bottom()


d = .005  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal


fig1.savefig('pps1.png')

if gnu_active == 0:
	plt.show()

