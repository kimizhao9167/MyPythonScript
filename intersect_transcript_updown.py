# input the intersect file from bedtools intersect
# output the bed file for up- and down-stream sequences 
import re
import sys
import shelve
import class_GTF
from class_GTF import Transcript
from class_GTF import getinfo

# input the annotation file
TransDB = shelve.open(sys.argv[3])
GTF = open(sys.argv[1],'r')
for line in GTF:
	m = re.match('^#',line)
	if m is None: # Not a comment line
		if line.split('\t')[2]=='transcript':
		# A line for transcript, init
			InfoString = line.split('\t')[8]	
			TransID = getinfo(InfoString,'transcript_id')
			GeneID = getinfo(InfoString,'gene_id')
			GeneType = getinfo(InfoString,'gene_biotype')
			Chromosome = line.split('\t')[0]
			Strand = line.split('\t')[6]
			trans = Transcript(TransID,GeneID,GeneType,Chromosome,Strand)
			TransDB[TransID] = trans
		if line.split('\t')[2]=='exon':
		# A line for exon, attach it to corresponding transcript
			InfoString = line.split('\t')[8]	
			TransID = getinfo(InfoString,'transcript_id')
			ExonID = getinfo(InfoString,'exon_id')
			ExonNumber = int(getinfo(InfoString,'exon_number'))
			ExonStart = int(line.split('\t')[3])
			ExonEnd = int(line.split('\t')[4])
			trans = TransDB[TransID]
			trans.myexon(ExonID,ExonStart,ExonEnd,ExonNumber)
			TransDB[TransID] = trans

# input the intersect file
upstream = 12
downstream = 12
InFile = open(sys.argv[2],'r')
Interc = InFile.readlines()
for ix in range(len(Interc)):
	prev = '' if ix==0 else Interc[ix-1].split('\t')[3]
	nex = '' if ix==len(Interc)-1 else Interc[ix+1].split('\t')[3]
	if Interc[ix].split('\t')[6]!='.' and Interc[ix].split('\t')[3]!=prev and Interc[ix].split('\t')[3]!=nex:
	# keep only uniq intersection reads
		InfoString = Interc[ix].split('\t')[14]
		TransID = getinfo(InfoString,'transcript_id')
		ExonID = getinfo(InfoString,'exon_id')
		trans = TransDB[TransID]
		pos = int(Interc[ix].split('\t')[2])
		updown = trans.updownloc(pos,upstream,downstream)
		for each in updown:
			print(trans.Chromosome,each-1,each,Interc[ix].split('\t')[3],'0',trans.Strand,sep='\t')
TransDB.close()
