from matplotlib import pyplot as plt
import sys
import numpy

rint=1000000

def parsing(readfile, acl_ct = []):

	acl_ct = []
	n_p=0
	for line in readfile:
	    vec=0
	    clk=0
	    count=0
	    if n_p > rint: break
	    for s in line.split():
		count=count+1
		if (count==1):
			vec=int(s)
			if (vec <= 255 or vec>= 300): break
			n_p=n_p+vec
		else:
			clk=int(s)/vec
			acl_ct.append(clk)
			vec=0

	readfile.close
	#acl = trimming(acl_ct, numpy.percentile(acl_ct,5), numpy.percentile(acl_ct,95))
	#acl = trimming(acl_ct, numpy.percentile(acl_ct,1), numpy.percentile(acl_ct,99))

	print(str(n_p))	

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
        f5 = str(sys.argv[5])
        f6 = str(sys.argv[6])

        fr1 = open(f1, 'r')
        fr2 = open(f2, 'r')
        fr3 = open(f3, 'r')
        fr4 = open(f4, 'r')
        fr5 = open(f5, 'r')
        fw = open(f6, 'w')

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

acl_ct5 = []
acl_ct5 = parsing(fr5)

for a,b,c,d,e in zip(acl_ct1, acl_ct2,  acl_ct3, acl_ct4, acl_ct5):
    #print(str(a) + ' ' + str(b) + ' ' + str(c) + ' ' + str(d))
    fw.write(str(a) + ' ' + str(b) + ' ' + str(c) + ' ' + str(d) + ' ' + str(e) + '\n')

fw.close
