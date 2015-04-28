# construct the input file for RNAduplex
# random shuffle the sequence of let-7a/7b
import sys
import re
import random
import os
let7a = 'TGAGGTAGTAGGTTGTATAGTT'
#let7a = 'GGGTGTAGATTTTAGTTGGGGT'
let7a = let7a.replace('U','T')
slet7a = ''.join(random.sample(let7a,len(let7a)))
InFile = open(sys.argv[1],'r')
lines = InFile.readlines()
OutFileName = 'random/'+'slet7a_'+slet7a+'.duplex'
OutFile = open(OutFileName,'w')
for ix in range(len(lines)):
	m = re.match('^>',lines[ix])
	if m is not None:
		name = lines[ix].replace('\n','')
	else:
		seq = lines[ix].replace('\n','')
		outline = name + '_'+ seq+'\n'+seq + '\n' + '>slet7a'+'_'+slet7a+'\n'+slet7a+'\n'
		OutFile.write(outline)
InFile.close()
OutFile.close()

# use RNAduplex to fold
RNAduplexOut = OutFileName + '.RNAduplex'
Command1 = 'RNAduplex < ' + OutFileName + ' > ' + RNAduplexOut
os.system(Command1)
FinalOut = RNAduplexOut + '.10th'
Command2 = 'python3 RNAduplex_let7_10th.py ' + RNAduplexOut + ' > ' + FinalOut
os.system(Command2)
