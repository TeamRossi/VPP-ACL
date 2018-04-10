from matplotlib import pyplot as plt
import sys
import math
import numbers
import json
import numpy as np
from scipy.interpolate import interp1d
from matplotlib.ticker import ScalarFormatter


def loaderConf(conf_script): 

	container={}
	cline=-1
	tmp_container={'gui':'', 'style':'', 'fig1':{}, 'fig2':{}}
	for line in conf_script:
		line = line.replace('\n','')
		ccolumn=0
		cline=cline+1
		if cline == 0:
			tmp_container['gui'] = str(line)
		if cline == 1:
			tmp_container['style'] = str(line)
		if cline == 2:
			#container={'type':'','title':'', 'namefile':'', 'log':''}
			line = line.replace("'", "\"")
			tmp_container['fig1'] = json.loads(line)
		if cline == 3:
			line = line.replace("'", "\"")
			tmp_container['fig2'] = json.loads(line)

	container = tmp_container

	conf_script.close

	return container

def loaderFile(file_script): 

	container=[]
	cline=0
	for line in file_script:
		line = line.replace('\n','')
		ccolumn=0
		cline=cline+1
		tmp_container={'path':'', 'type':'', 'label':''}
		for s in line.split(','):
			if ccolumn == 0:
				tmp_container['path'] = str(s)
			if ccolumn == 1:
				tmp_container['type'] = str(s)
			if ccolumn == 2:
				tmp_container['label'] = str(s)
			if ccolumn == 3:
				tmp_container['color'] = str(s)

			ccolumn = ccolumn + 1
		cline=cline + 1
		container.append(tmp_container)

	file_script.close

	return container


def loaderIndex(readfile, l_container={}): 

	l_container = {'size':[], 'index':[], 'ord_ind':[], 'ht_a':[],'col':[], 'accesses':[]}
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
						element = l_container['ord_ind']
						element.append(float(s))
					if cline == 3:
						element = l_container['ht_a']
						element.append(float(s))
					if cline == 2:
						element = l_container['col']
						element.append(float(s))
					if cline == 4:
						element = l_container['accesses']
						element.append(float(s))
				else :
					if cline == 1:
						element = l_container['ord_ind'][(count-1)]
						element = element +float(s)
						l_container['ord_ind'][(count-1)] = element
					if cline == 3:
						element = l_container['ht_a'][(count-1)]
						element = element +float(s)
						l_container['ht_a'][(count-1)] = element
					if cline == 2:
						element = l_container['col'][(count-1)]
						element = element +float(s)
						l_container['col'][(count-1)] = element
					if cline == 4:
						element = l_container['accesses'][(count-1)]
						element = element +float(s)
						l_container['accesses'][(count-1)] = element

				count = count + 1
			else: count = count + 1
		cline=cline + 1
		count=0
		if cline > 4: 
		   	cline=-1
			firstime = firstime + 1





	readfile.close

	for column in range(len(l_container['size'])):
		element = l_container['ord_ind'][(column-1)]
		element = element/firstime
		l_container['ord_ind'][(column-1)] = element
		element = l_container['ht_a'][(column-1)]
		element = element/firstime
		l_container['ht_a'][(column-1)] = element
		element = l_container['col'][(column-1)]
		element = element/firstime
		l_container['col'][(column-1)] = element
		element = l_container['accesses'][(column-1)]
		element = element/firstime
		l_container['accesses'][(column-1)] = element
	return l_container


def seed_interpol(seed_line):
	seed_interpol=[]
	
	x=[1000, 2000, 4000, 8000, 16000, 32000, 64000]
	y=seed_line
	print("Seed-interpol: " + str(seed_line))

	#f_interpol = interp1d(x, y, kind='cubic') 
	f_interpol = interp1d(x, y, kind='linear') 

	xnew=[]
	for i,j in zip([1000, 2000, 4000, 8000, 16000, 32000], [2000, 4000, 8000, 16000, 32000, 64000]):
		xnew = xnew + list(np.linspace(i, j, num=4, endpoint=False))
	xnew.append(64000)
	seed_interpol = f_interpol(xnew)
	
	return seed_interpol,xnew,x


try:
        print("file1: \t" + str(sys.argv[1]))
        print("file2: \t" + str(sys.argv[2]))

        f1 = str(sys.argv[1])
        f2 = str(sys.argv[2])

        fconf = open(f1, 'r')
        finfo = open(f2, 'r')

except IndexError:
        print("Error: no Filename")
        sys.exit(2)


files_info=[]
files_info = loaderFile(finfo)

conf_info=[]
conf_info = loaderConf(fconf)

print(str(files_info))
print(str(conf_info))

if conf_info['style'] == 'slide':
	plt.style.use('valerio-slide')
	fig1, ax1 = plt.subplots(figsize=(14,8))
	fig2, ax2 = plt.subplots(figsize=(14,8))
else:
	fig1, ax1 = plt.subplots(figsize=(8,6))
	fig2, ax2 = plt.subplots(figsize=(8,6))

typea=str(conf_info['fig1']['type'])
typeb=str(conf_info['fig2']['type'])

for single_file in files_info:
	seed_line = {}
        open_file = open(single_file['path'], 'r')

	seed_line = loaderIndex(open_file)

	print(str(single_file))

	seeda, xa , x1 = seed_interpol(seed_line[typea])
	seedb, xb , x2 = seed_interpol(seed_line[typeb])

	ax1.plot(xa, seeda, str(single_file['color']), label=single_file['label'])
	ax2.plot(xb, seedb, str(single_file['color']), label=single_file['label'])

#====== Figure 1 specification
ax1.set_xlabel('Ruleset size')
if conf_info['fig1']['type'] != 'class':
	ax1.set_ylabel(str(conf_info['fig1']['y-label']))
else:
	ax1.set_ylabel(u'${\mu}s$')



if conf_info['fig1']['x-log'] == 'on':
	ax1.set_xscale("log", basey=2)
if conf_info['fig1']['y-log'] == 'on':
	ax1.set_yscale("log", basey=10)
	ax1.yaxis.set_major_formatter(ScalarFormatter())


ax1.set_xticks(x1)
ax1.set_xticklabels(['1K','2K','4K','8K','16K','32K','64K'])

ax1.set_axisbelow(True)
ax1.xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
ax1.yaxis.grid(color='gray', linestyle='dashed', linewidth=1)

#ax.set_ylim([0,6.5])
#ax.set_ylim([0,1])
ax1.set_title(str(conf_info['fig1']['title']))

handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[::-1], labels[::-1])

fig1.savefig(str(conf_info['fig1']['namefile']))

#====== Figure 2 specification
ax2.set_xlabel('Ruleset size')
if conf_info['fig2']['type'] != 'class':
	ax2.set_ylabel(str(conf_info['fig2']['y-label']))
else:
	ax2.set_ylabel(u'${\mu}s$')

if conf_info['fig2']['x-log'] == 'on':
	ax2.set_xscale("log", basex=2)
if conf_info['fig2']['y-log'] == 'on':
	ax2.set_yscale("log", basey=10)


ax2.set_xticks(x2)
ax2.set_xticklabels(['1K','2K','4K','8K','16K','32K','64K'])

ax2.set_axisbelow(True)
ax2.xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
ax2.yaxis.grid(color='gray', linestyle='dashed', linewidth=1)

handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles[::-1], labels[::-1])

ax2.set_title(str(conf_info['fig2']['title']))

fig2.savefig(str(conf_info['fig2']['namefile']))

if conf_info['gui'] == 'on':
	plt.show()

