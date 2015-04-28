# input the RNAduplex results
# output energy

from RNAduplex_parser import RNAduplex
import sys

InFile = open(sys.argv[1],'r')
Lines = InFile.readlines()
for ix in (range(len(Lines)-2)):
	if ix%3==0:
		t = RNAduplex(Lines[ix],Lines[ix+1],Lines[ix+2])
		# location 13 corresponding to the 5'end of reads
		# i.e. the cleavage site
		print(t.ID1.replace('>',''),t.Energy,t.getpairing(13)[0],t.getpairing(13)[1],t.getpairing(13)[2],t.getpairing(13)[3],sep='\t')
