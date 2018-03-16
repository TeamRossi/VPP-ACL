from matplotlib import pyplot as plt
import sys
import numpy

rint=1000000

def parsing(readfile, acl_ct = []):

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

#print(str(acl_ct1))

acl_ct2 = []
acl_ct2 = parsing(fr2)

acl_ct3 = []
acl_ct3 = parsing(fr3)

acl_ct4 = []
acl_ct4 = parsing(fr4)

print(str(len(acl_ct1))+ " " +str(len(acl_ct2))+ " " +str(len(acl_ct3))+ " " +str(len(acl_ct4))+ " " )



plt.style.use('valerio-slide')
#fig = plt.figure()
fig, ax = plt.subplots()

data = (acl_ct1 + acl_ct2 + acl_ct3 + acl_ct4)
binwidth=10
#binwidth=300
bins_l=numpy.arange(min(data), max(data) + binwidth, binwidth)

plt.hist(acl_ct1, bins=bins_l, label="1k ruleset")
plt.hist(acl_ct2, bins=bins_l, label="2k ruleset")
plt.hist(acl_ct3, bins=bins_l, label="4k ruleset")
plt.hist(acl_ct4, bins=bins_l, label="8k ruleset")


# add some text for labels, title and axes ticks
#ax.set_xticklabels(ax.get_xticklabels(),rotation=30)
#ax.set_xlim([0,60000])
ax.set_xlabel('Clock cycle')
ax.set_ylabel('Density')
ax.set_title('Classification time')

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])

plt.savefig('hist_1m.png')
#plt.show()


print("=================================")
print("Table:")
data = [acl_ct1, acl_ct2, acl_ct3, acl_ct4]

rows = ("Avg", "Std")
columns = ("1K", "2K", "4K", "8K")

data_t = [[numpy.mean(acl_ct1),numpy.mean(acl_ct2), numpy.mean(acl_ct3), numpy.mean(acl_ct4)], 
	[numpy.std(acl_ct1),numpy.std(acl_ct2), numpy.std(acl_ct3), numpy.std(acl_ct4)]]

fw = open("tmp.out", 'w')
out_str="size:\t1K\t2K\t4K\t8K\n"
print out_str
fw.write(out_str)

for j in range(len(rows)):
	out_str = str(rows[j])+ ":\t"
	#print str(rows[j])+ ": \t"
	for i in range(len(columns)):
		out_str = out_str + str(round(data_t[j][i],3)) + "\t"
		#print str(data_t[j-1][i-1]) + " \t "
	out_str = out_str + "\n"
	#print "\n"
	print out_str
	fw.write(out_str)

fw.close()

