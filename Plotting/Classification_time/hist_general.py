from matplotlib import pyplot as plt
import matplotlib as mpl
import json
import sys
import numpy

rint=1000000
frequency=2.6*1000


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




def parsing(readfile, acl_ct = []):

	acl_ct = []
	for line in readfile:
	    for s in line.split():
		clock_cycle = int(s)
		microseconds = float(clock_cycle / frequency)
		acl_ct.append(microseconds)

	readfile.close
	#acl = trimming(acl_ct, numpy.percentile(acl_ct,5), numpy.percentile(acl_ct,95))
	#acl = trimming(acl_ct, numpy.percentile(acl_ct,1), numpy.percentile(acl_ct,99))

	#return acl
	return acl_ct

def trimming(acl_ct, perc_low, perc_high):
	acl=[]
	for ele in acl_ct:
		if not(ele < perc_low or ele > perc_high):
			acl.append(ele)
	return acl


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
else:   
        width = 11
        height = width / 1.618
        params = {
           'axes.labelsize': 20,
           'font.size': 20,
           'legend.fontsize': 18,
           'xtick.labelsize': 18,
           'ytick.labelsize': 18,
           'text.usetex': False,
           'figure.figsize': [width, height]
           }
        mpl.rcParams.update(params)
        fig1, ax1 = plt.subplots()

data = []
for single_file in files_info:
        open_file = open(single_file['path'], 'r')

	acl_ct = []
	acl_ct = parsing(open_file)
	
	data = (data + acl_ct)

binwidth = float(conf_info['fig1']['binwidth'])
bins_l = numpy.arange(min(data), max(data) + binwidth, binwidth)

for single_file in files_info:
        open_file = open(single_file['path'], 'r')

	acl_ct = []
	acl_ct = parsing(open_file)
	plt.hist(acl_ct, bins=bins_l, label=single_file['label'])


ax1.set_xlim(conf_info['fig1']['xlim'])

if conf_info['fig1']['type'] != 'us':
	ax1.set_xlabel(str(conf_info['fig1']['x-label']))
else:
	ax1.set_xlabel(u'${\mu}s$')

ax1.set_ylabel('Frequency')

ax1.set_title(str(conf_info['fig1']['title']))

handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[::-1], labels[::-1])

fig1.savefig(str(conf_info['fig1']['namefile'])+'.svg', format='svg', bbox_inches='tight')
fig1.savefig(str(conf_info['fig1']['namefile'])+'.png', format='png', bbox_inches='tight')
fig1.savefig(str(conf_info['fig1']['namefile'])+'.pdf', format='pdf', bbox_inches='tight')


if conf_info['gui'] == 'on':
	plt.show()
