# construct the input file for RNAduplex
import sys
import re
let7a = 'UGAGGUAGUAGGUUGUAUAGUU'
let7a = let7a.replace('U','T')
InFile = open(sys.argv[1],'r')
lines = InFile.readlines()
for ix in range(len(lines)):
	m = re.match('^>',lines[ix])
	if m is not None:
		name = lines[ix].replace('\n','')
	else:
		seq = lines[ix].replace('\n','')
		print(name + '_'+ seq,seq,'>let7a'+'_'+let7a,let7a,sep='\n')
