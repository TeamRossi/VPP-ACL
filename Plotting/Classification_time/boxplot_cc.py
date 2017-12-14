from matplotlib import pyplot as plt
import sys
import numpy


rint=1000000

def parsing(readfile):

	acl_ct = []
	for line in readfile:
	    for s in line.split():
		acl_ct.append(int(s))


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

	f1 = str(sys.argv[1])
        f2 = str(sys.argv[2])
        f3 = str(sys.argv[3])
        f4 = str(sys.argv[4])

        fr1 = open(f1, 'r')
        fr2 = open(f2, 'r')
        fr3 = open(f3, 'r')
        fr4 = open(f4, 'r')

except IndexError:
	print("Error: no Filename")
	sys.exit(2)



print("parsing")
acl_ct1 = []
acl_ct1 = parsing(fr1)


acl_ct2 = []
acl_ct2 = parsing(fr2)

acl_ct3 = []
acl_ct3 = parsing(fr3)

acl_ct4 = []
acl_ct4 = parsing(fr4)


plt.style.use('valerio-slide')
#fig = plt.figure()
fig, ax = plt.subplots(figsize=(12,9))

data = [acl_ct1, acl_ct2, acl_ct3, acl_ct4]

bplot = ax.boxplot(data, vert=True)   # fill with color)

ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dashed')

# add some text for labels, title and axes ticks
plt.xticks(list(range(1,5)),['1K','2K','4K','8K'])
ax.set_xticklabels(ax.get_xticklabels(),rotation=30)
ax.set_xlabel('Ruleset Size')
ax.set_ylabel('Clock cycle')
#ax.xaxis.set_ticks(acl_index.keys())
ax.set_title('Classification time')

plt.savefig('boxplot.png')

plt.show()
