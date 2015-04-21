# get the length distribution of a seq file
# support format: fastq,fasta
from Bio import SeqIO
import sys
handle = SeqIO.parse(sys.argv[1],sys.argv[2])
for each in handle:
	print(len(each))
