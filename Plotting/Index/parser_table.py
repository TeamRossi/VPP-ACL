import numbers
import sys
import numpy
import math


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



def parsing(readfile, res = {}):

	acl_ct = {'index':[], 'ord_ind':[], 'ht_a':[],'col':[], 'accesses':[]}
	acl_final = {'index':[], 'ord_ind':[], 'ht_a':[],'col':[], 'accesses':[]}
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
	

	for type in acl_ct.keys():
		acl_final[type]=numpy.mean(acl_ct[type])

	return acl_final


try:
        print("file1: \t" + str(sys.argv[1]))
        print("file2: \t" + str(sys.argv[2]))

        f1 = str(sys.argv[1])
        f2 = str(sys.argv[2])

        fw = open(f2, 'w')
        finfo = open(f1, 'r')

except IndexError:
        print("Error: no Filename")
        sys.exit(2)


files_info=[]
files_info = loaderFile(finfo)

summary = {'index':[], 'ord_ind':[], 'ht_a':[],'col':[], 'accesses':[]}

c_line = 0
for single_file in files_info: 
	c_line = c_line + 1
        open_file = open(single_file['path'], 'r') 
 
        acl_ct = {} 

	if single_file['type'] == 'vpp':
		acl_ct = parsing(open_file) 
	if single_file['type'] == 'sw':
		acl_ct = parsingSW(open_file) 
         
	print(str(acl_ct))
	for type in summary.keys():
		summary[type].append(acl_ct[type])	


sizes = ['1K','2K','4K','8K','16K','32K','64K']

fw.write("Size:\t") 
for i in sizes:
	fw.write(str(i) + '\t') 
fw.write("\n") 

fw.write("Lookup_id\t") 
for i in summary['ord_ind']:
	fw.write(str(i) + '\t') 
fw.write("\n") 

fw.write("HT-accesses\t") 
for i in summary['ht_a']:
	fw.write(str(i) + '\t') 
fw.write("\n") 

fw.write("Collisions\t") 
for i in summary['col']:
	fw.write(str(i) + '\t') 
fw.write("\n") 

fw.write("Tot-accesses\t") 
for i in summary['accesses']:
	fw.write(str(i) + '\t') 
fw.write("\n") 

fw.close
