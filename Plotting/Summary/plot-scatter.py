from matplotlib import pyplot as plt
import matplotlib as mpl
import sys
import math
import numbers
import numpy as np
import json

from scipy.interpolate import interp1d
from matplotlib.ticker import ScalarFormatter


def loaderPaper(readfile, l_container={}): 

	l_container={'size':[], 'class':[], 'part':[], 'cons':[], 'quer':[]}
	cline=-1
	counter=0
	firstime=0
	for line in readfile:
		for s in line.split():
			element = []
			count = counter - 4
			if counter > 4 and counter < 11:
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
				counter = counter + 1
			else: counter = counter + 1
		cline=cline + 1
		counter=0
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
                        if ccolumn == 4:
                                tmp_container['linestyle'] = str(s)
                        if ccolumn == 5:
                                tmp_container['marker'] = str(s)
                        if ccolumn == 6:
                                tmp_container['fillstyle'] = str(s)

                        ccolumn = ccolumn + 1
                cline=cline + 1
                container.append(tmp_container)

        file_script.close

        return container

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
        width = 7.5
        height = width / 1.618
        params = {
           'axes.labelsize': 16,
           'font.size': 16,
           'legend.fontsize': 13,
           'xtick.labelsize': 13,
           'ytick.labelsize': 13,
           'text.usetex': False,
           'figure.figsize': [width, height]
           }
        mpl.rcParams.update(params)
        fig1, ax1 = plt.subplots()

typea=str(conf_info['fig1']['type'])

print("Types: "+ typea)

for single_file in files_info:
        seed_line = {}
        open_file = open(single_file['path'], 'r')

        if single_file['type'] == 'vpp':
                seed_line = loaderVpp(open_file)

        if single_file['type'] == 'vpp-tot':
                seed_line = loaderVppTot(open_file)

        if single_file['type'] == 'paper':
                seed_line = loaderPaper(open_file)

        if single_file['type'] == 'paper-tot':
                #seed_line = loaderPaperTot(open_file)
		print("error")

        print(str(single_file))
        print(str(seed_line))

	seeda = np.average(seed_line['cons'])
	seedb = np.average(seed_line['class'])
	#area = np.pi*155*np.std(seed_line['class'])/np.linalg.norm(seed_line['class']) 
	area = np.pi*55
	print(str(single_file['label'])+": "+str(seeda)+"-"+str(seedb)+"; "+str(area))
	ax1.scatter(seedb, seeda, s=area, alpha=0.75, label=single_file['label'])


if conf_info['fig1']['x-log'] == 'on':
        ax1.set_xscale("log", basey=10)
        ax1.xaxis.set_major_formatter(ScalarFormatter())
if conf_info['fig1']['y-log'] == 'on':
        ax1.set_yscale("log", basey=10)
        ax1.yaxis.set_major_formatter(ScalarFormatter())


ax1.set_ylabel('Update Time ' + u'$(ms)$')
ax1.set_xlabel('Classification Time ' + u'$({\mu}s)$')

ax1.set_axisbelow(True)
ax1.xaxis.grid(color='gray', linestyle='dashed', linewidth=1)
ax1.yaxis.grid(color='gray', linestyle='dashed', linewidth=1)


ax1.set_ylim(3, 20000)  # outliers only
ax1.set_xlim(0.25, 2.25)  # outliers only
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[::-1], labels[::-1])



fig1.savefig(str(conf_info['fig1']['namefile'])+'.svg', format='svg', bbox_inches='tight')
fig1.savefig(str(conf_info['fig1']['namefile'])+'.png', format='png', bbox_inches='tight')
fig1.savefig(str(conf_info['fig1']['namefile'])+'.pdf', format='pdf', bbox_inches='tight')


if conf_info['gui'] == 'on':
        plt.show()

