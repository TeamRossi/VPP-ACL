from matplotlib import pyplot as plt
import sys
import numpy
import math
import numbers
import json
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

def parsingSW(readfile, res = {}):

	acl_ct = {'index':[], 'ord_ind':[], 'ht_a':[],'col':[], 'accesses':[]}
	count=0
	for line in readfile:
	    count=count+1
	    for s in line.split('-'):
		if s.isdigit():
			if (count==36):
				element=acl_ct['ht_a']
				element.append(int(s))

	count=-1
	for x in acl_ct['ht_a']:
		count=count+1
		element=acl_ct['ord_ind']
		for i in range(1,x):
			element.append(count)
	readfile.close

	return acl_ct


def parsing(readfile, res = {}):

	acl_ct = {'index':[], 'ord_ind':[], 'ht_a':[],'col':[], 'accesses':[]}
	no_firstline=0
	for line in readfile:
	    if no_firstline < 3:
		no_firstline = no_firstline +1
		continue
	    count=0
	    for s in line.split():
		if s.isdigit():
			count=count+1
			element = []
			if (count==1):
				element=acl_ct['index']
				element.append(int(s))
			if (count==2):
				element=acl_ct['ord_ind']
				element.append(int(s))
			if (count==3):
				element=acl_ct['ht_a']
				element.append(int(s))
			if (count==4):
				element=acl_ct['col']
				element.append(int(s))

	readfile.close

	for x,y in zip(acl_ct['ht_a'], acl_ct['col']):
		element=acl_ct['accesses']
		element.append(int(x+y))

	return acl_ct



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


typea=str(conf_info['fig1']['type'])

print("Types: " + typea )

data=[]

for single_file in files_info: 
        open_file = open(single_file['path'], 'r') 
 
        acl_ct = {} 

	if single_file['type'] == 'vpp':
		acl_ct = parsing(open_file) 
	if single_file['type'] == 'sw':
		acl_ct = parsingSW(open_file) 
         
        data = (data + acl_ct[typea]) 
 
binwidth = int(conf_info['fig1']['binwidth'] )
bins_l = numpy.arange(min(data), max(data) + binwidth, binwidth) 
 
for single_file in files_info: 
        open_file = open(single_file['path'], 'r') 
 
        acl_ct = {} 
	if single_file['type'] == 'vpp':
		acl_ct = parsing(open_file) 
	if single_file['type'] == 'sw':
		acl_ct = parsingSW(open_file) 
        plt.hist(acl_ct[typea], alpha=0.5, bins=bins_l, label=single_file['label']) 
 
 
#ax1.set_xlim(conf_info['fig1']['xlim']) 
 
if conf_info['fig1']['type'] != 'class': 
        ax1.set_xlabel(str(conf_info['fig1']['x-label'])) 
else: 
        ax1.set_xlabel(u'${\mu}s$') 
 
ax1.set_ylabel('Density') 
 
ax1.set_title(str(conf_info['fig1']['title'])) 
 
handles, labels = ax1.get_legend_handles_labels() 
ax1.legend(handles[::-1], labels[::-1]) 
 
fig1.savefig(str(conf_info['fig1']['namefile'])) 
 
if conf_info['gui'] == 'on': 
        plt.show() 




