# input gtf file, output gtf file with specified feature type

import sys
import re

gtf = open(sys.argv[1],'r')
for line in gtf:
	m = re.search('^#',line)
	if m is not None or line.split('\t')[2]==sys.argv[2]:
		print(line,end='')
