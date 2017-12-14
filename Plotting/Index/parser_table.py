import numbers
import sys


def loader_class(readfile, l_container={}): 

	l_container = {'count':[], 'shadowed':[],'range':[], 'ran_list':[], 'sha_list':[]}
	cline=0
	for line in readfile:
	    count=0
	    for s in line.split():
		element=[]
		try:
			if isinstance(float(s), numbers.Real):
				if cline == 0:
					element = l_container['count'] 
					element.append(round(float(s)))
					cline = cline + 1
				elif cline == 1:
					element = l_container['shadowed'] 
					element.append(round(float(s)))
					cline = cline + 1
				elif cline == 2:
					element = l_container['sha_list']
					element.append(round(float(s)))
					cline = cline + 1
				elif cline == 3:
					element = l_container['range'] 
					element.append(round(float(s)))
					cline = cline + 1
				elif cline == 4:
					element = l_container['ran_list'] 
					element.append(round(float(s)))
					cline = 0 
		except ValueError: count = count

	readfile.close

	return l_container



try:
        print("file1: \t" + str(sys.argv[1]))
        print("file2: \t" + str(sys.argv[2]))

        f1 = str(sys.argv[1])
        f2 = str(sys.argv[2])

        fr1 = open(f1, 'r')
        fw = open(f2, 'w')
except IndexError:
        print("Error: no Filename")
        sys.exit(2)


file_line = {}
file_line = loader_class(fr1)


print(str(file_line))

sizes = ['1K','2K','4K','8K','16K','32K']

fw.write("Size:\t") 
for i in sizes:
	fw.write(str(i) + '\t') 
fw.write("\n") 

fw.write("Lookup\t") 
for i in file_line['count']:
	fw.write(str(i) + '\t') 
fw.write("\n") 

fw.write("Shadowed\t") 
for i in file_line['shadowed']:
	fw.write(str(i) + '\t') 
fw.write("\n") 

fw.write("Sha_lookup\t") 
for i in file_line['sha_list']:
	fw.write(str(i) + '\t') 
fw.write("\n") 

fw.write("PortRange\t") 
for i in file_line['range']:
	fw.write(str(i) + '\t') 
fw.write("\n") 

fw.write("PR_lookup\t") 
for i in file_line['ran_list']:
	fw.write(str(i) + '\t') 
fw.write("\n") 

fw.close
