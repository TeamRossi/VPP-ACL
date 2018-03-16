import numbers
import sys


def loader_thr(readfile, l_container={}): 

	l_container={'TX':[], 'RX':[]}
	cline=0
	mrx=0
	mtx=0
	for line in readfile:
	    count=0
	    for s in line.split():
		element = []
		if (count == 0):
			mrx = mrx + float(s)
			if cline == 4:
				mrx = mrx / 5
				element = l_container['RX']
				element.append(float(mrx))
				mrx=0
		if (count == 1):
			mtx = mtx + float(s)
			if cline == 4:
				mtx = mtx / 5
				element = l_container['TX']
				element.append(float(mtx))
				mtx=0
				cline = 0 
                        else: cline=cline + 1
		count=count+1

	readfile.close

	element = []
	element = l_container['RX']
#	element.append(int(0))
	element = []
	element = l_container['TX']
#	element.append(int(0))
	return l_container


def loader_class(readfile, l_container={}): 

	l_container={'clock':[], 'us':[]}
	cline=0
	for line in readfile:
	    count=0
	    for s in line.split():
		element = []
		try:
			if isinstance(float(s), numbers.Real):
				if cline == 0:
					element = l_container['clock']
					element.append(round(float(s),3))
					cline = cline + 1
				elif cline == 1:
					element = l_container['us']
					element.append(round(float(s),3))
					cline = 0 
		except ValueError: count = count

	readfile.close

	return l_container


def loader_part(readfile, l_container=[]): 

	l_container=[]
	cline=0
	avg_part = 0
	for line in readfile:
	    for s in line.split():
		if s.isdigit():
			avg_part = avg_part + int(s)
			if cline == 4:
				avg_part = avg_part/5
				l_container.append(int(avg_part))
				cline = 0 
				avg_part = 0
			else: cline = cline + 1

	readfile.close

	return l_container



try:
        print("file1: \t" + str(sys.argv[1]))
        print("file2: \t" + str(sys.argv[2]))
        print("file3: \t" + str(sys.argv[3]))
        print("file4: \t" + str(sys.argv[4]))

        f1 = str(sys.argv[1])
        f2 = str(sys.argv[2])
        f3 = str(sys.argv[3])
        f4 = str(sys.argv[4])

        fr1 = open(f1, 'r')
        fr2 = open(f2, 'r')
        fr3 = open(f3, 'r')
        fw = open(f4, 'w')
except IndexError:
        print("Error: no Filename")
        sys.exit(2)


file1_line = {}
file1_line = loader_thr(fr1)

file2_line = {}
file2_line = loader_class(fr2)

file3_line = {}
file3_line = loader_part(fr3)


print(str(file1_line))
print(str(file2_line))
print(str(file3_line))

sizes = ['1','10','100','500','1K','2K','4K','8K','16K','32K']

fw.write("Size:\t") 
for i in sizes:
    fw.write(str(i) + '\t') 
fw.write("\n") 

fw.write("Throughput:\t") 
for i in file1_line['RX']:
    fw.write(str(i) + '\t') 
fw.write("\n") 

fw.write("Microseconds:\t") 
for i in file2_line['us']:
    fw.write(str(i) + '\t') 
fw.write("\n") 

fw.write("Clock_cycle:\t") 
for i in file2_line['clock']:
    fw.write(str(i) + '\t') 
fw.write("\n") 

fw.write("Partition:\t") 
for i in file3_line:
    fw.write(str(i) + '\t') 
fw.write("\n") 

fw.close
