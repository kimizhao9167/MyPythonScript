# input a sam file, output position of the first matching base in a bed file
# keep only the alignment with at least 10 match at the first segment of 5' 

import sys
import re

file = open(sys.argv[1],'r')
for each in file:
	loc = -1
	if each.split()[1]=='0': # mapping to positive strand is easily handled 
		m = re.search('^[1-9][0-9]M',each.split()[5])
		sign = '+'
		if m is not None:
			loc = each.split()[3]

	if each.split()[1]=='16': # mapping to reverse strand needs some calculation
		m = re.search('(^[1-9][0-9])(M$)',each.split()[5]) # no introns and no clipping
		if m is not None:
			loc = int(each.split()[3]) + int(m.group(1)) - 1
		m = re.search('^[0-9]+S([1-9][0-9])M$',each.split()[5]) # no introns and clipping at the 3'end
		if m is not None:
			loc = int(each.split()[3]) + int(m.group(1)) - 1
		m = re.search('([0-9]+)M([0-9]+)N([1-9][0-9])M$',each.split()[5]) # have intron and no/have clipping at the 3'end
		if m is not None:
			loc = int(each.split()[3]) + int(m.group(1)) + int(m.group(2)) + int(m.group(3)) - 1
		sign = '-'

	if loc!=-1:
		print(each.split()[2],int(loc)-1,loc,each.split()[0],'0',sign,sep='\t')
	
