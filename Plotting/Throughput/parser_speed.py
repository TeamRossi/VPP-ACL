import sys
import numbers

try:
	print("read file: \t" + str(sys.argv[1]))
	print("write file: \t" + str(sys.argv[2]))

	filenamer = str(sys.argv[1])
	filenamew = str(sys.argv[2])

	fr = open(filenamer, 'r')
	fw = open(filenamew, 'w')
except IndexError:
	print("Error: no Filename")
	sys.exit(2)

val_line={}
inside=False
count=0
for line in fr:
        if (not line.find("==========V=============") and inside):
		inside=False

	if inside:
		element = []
                for s in line.split():
			try:
				if isinstance(float(s), numbers.Real):
			       # if s.is_digit(): 
					element.append(s)
			except ValueError: count = count
		val_line[count] = element
		count = count + 1

        if (not line.find("==========VVV=============") and not inside):
		inside=True

#	print(str(line) + str(inside) + str(count))

print(str(val_line))
#str_tow = "RX-X TX-X RX-Y TX-Y ..."
l_i = 0
while l_i < (len(val_line) -1):
	str_tow = ""
	for el_i in range(len(val_line[l_i])):
		str_tow = str_tow + val_line[l_i][el_i]  + " " + val_line[l_i+1][el_i]  + " "
	print(str(str_tow))
	l_i = l_i +2
        fw.write(str(str_tow) + '\n')

fr.close
fw.close
