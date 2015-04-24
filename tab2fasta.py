# input tab file, output fasta file
import sys
InFile = open(sys.argv[1],'r')
lines = InFile.readlines()
for ix in range(len(lines)):
	prev = lines[ix-1].split('\t')[0] if ix!=0 else ''
	now = lines[ix].split('\t')[0]
	if now!=prev:
		if prev!='':
			print('\n>'+now)
		else:
			print('>'+now)
	base = lines[ix].split('\t')[1]
	base = base.replace('\n','')
	print(base,end='')
