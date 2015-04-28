# input the RNAduplex results
# output energy

from RNAduplex_parser import RNAduplex
import sys

InFile = open(sys.argv[1],'r')
Lines = InFile.readlines()
for ix in (range(len(Lines)-2)):
	if ix%3==0:
		t = RNAduplex(Lines[ix],Lines[ix+1],Lines[ix+2])
		print(t.ID1,t.Energy,t.getpairing(13),sep='\t')
