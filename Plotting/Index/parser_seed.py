from matplotlib import pyplot as plt
import sys
import numpy


def parsing(readfile, res = {}):

	res = {'index':[], 'count':0, 'shadowed':0,'range':0, 'ran_list':0, 'sha_list':0}
	acl_ct = {'index':[], 'count':[], 'shadowed':[],'range':[], 'ran_list':[], 'sha_list':[]}
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
				element=acl_ct['count']
				element.append(int(s))
			if (count==3):
				flag = int(s) & 1
				element=acl_ct['shadowed']
				element.append(flag)
				if flag == 1: 
					element=acl_ct['sha_list']
					element.append(acl_ct['count'][-1]) 
			if (count==4):
				flag = int(s) & 1
				element=acl_ct['range']
				element.append(flag)
				if flag == 1: 
					element=acl_ct['ran_list']
					element.append(acl_ct['count'][-1]) 

	readfile.close

	element = []
	#element = acl_ct['index']

	element = []
	element = acl_ct['count']
	res['count'] = ((numpy.mean(element)))

	element = []
	element = acl_ct['shadowed']
	res['shadowed'] = (int(sum(element)))

	if int(sum(element)) != 0:
		element = []
		element = acl_ct['sha_list']
		res['sha_list'] = ((numpy.mean(element)))

	element = []
	element = acl_ct['range']
	res['range'] = (int(sum(element)))

	if int(sum(element)) != 0:
		element = []
		element = acl_ct['ran_list']
		res['ran_list'] = ((numpy.mean(element)))

	return res

try:

	f1 = str(sys.argv[1])
        f2 = str(sys.argv[2])

        fr1 = open(f1, 'r')
        fw1 = open(f2, 'aw')
except IndexError:
	print("Error: no Filename")
	sys.exit(2)



print("parsing")
acl_ct1 = {}
acl_ct1 = parsing(fr1)


#print(str(acl_ct1))

fw1.write("lookup_count " + str(acl_ct1['count']) + '\n')
fw1.write("shadowed_count " + str(acl_ct1['shadowed']) + '\n')
fw1.write("shadowed_avg " + str(acl_ct1['sha_list']) + '\n')
fw1.write("range_count " + str(acl_ct1['range']) + '\n')
fw1.write("range_avg " + str(acl_ct1['ran_list']) + '\n')

fw1.close

