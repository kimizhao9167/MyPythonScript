# input the intersect file from bedtools intersect
# output the gene types
# if not annotated, output as 'intergenic_regions'

import sys
infile = open(sys.argv[1],'r')
lines = infile.readlines()
for ix in range(len(lines)):
	if ix==0:
		prev = ''
	else:
		prev = lines[ix-1].split('\t')[3]
	if ix==len(lines)-1:
		nex = ''
	else:
		nex = lines[ix+1].split('\t')[3]
	if lines[ix].split('\t')[3] != prev and lines[ix].split('\t')[3] != nex:
	# drop intersect to overlapping genes:
		if(lines[ix].split('\t')[6]=='.'):
			genetype = 'gene_biotype "intergenic_regions"'
			geneid = 'NA'
		else:
			info = lines[ix].split('\t')[14]
			genetype = info.split(';')[4]
			geneid = info.split(';')[0]
		print(lines[ix].split('\t')[0],lines[ix].split('\t')[1],lines[ix].split('\t')[2],lines[ix].split('\t')[3],lines[ix].split('\t')[5],lines[ix].split('\t')[9],lines[ix].split('\t')[10],geneid,genetype,sep='\t')

