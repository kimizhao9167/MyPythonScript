# define classes related to GTF file

# a transcript class to store the info, including 
# transcript id, gene id, strand,exon count,exon id,exon loc
class Transcript:
	def __init__(self,TransID,GeneID,GeneType,Chromesome,Strand):
	# init when encount a line with feature name 'transcript'
	# input info from this line
		self.TransID = TransID
		self.GeneID = GeneID
		self.GeneType = GeneType
	#	self.Chromosome = Chromosome
		self.Strand = Strand
		self.ExonCount = 0
		self.Exons = {}
		self.UTR3 = {}
		self.UTR5 = {}

	def myexon(self,ExonID,ExonStart,ExonEnd,ExonNumber):
		# attach an exon to it
		self.Exons[ExonNumber-1]=[ExonID,ExonStart,ExonEnd]
		self.ExonCount += 1
	
	def getlength(self):
		length = 0
		for ix in range(self.ExonCount):
			length += self.Exons[ix][2]-self.Exons[ix][1] + 1
		return(length)
	
	def getrelativeloc(self,pos):
		# input position, get the relative location
		loc = 0
		if self.Strand=='+':
			for ix in range(self.ExonCount):
				if pos > self.Exons[ix][2]:
					loc = loc + self.Exons[ix][2] - self.Exons[ix][1] + 1
				else:
					loc = loc + pos - self.Exons[ix][1] + 1
					break
		else:
			for ix in range(self.ExonCount):
				if pos < self.Exons[ix][1]:
					loc = loc + self.Exons[ix][2] - self.Exons[ix][1] + 1
				else:
					loc = loc + self.Exons[ix][2] - pos + 1
					break
		return(loc/self.getlength())	


# define a getinfo function for a string
# input a string and wanted field
# output the value of the field
def getinfo(InfoString,field):
	import re
	items = InfoString.split(';')
	p = '.*' + field + ' "(.*)"'
	for EachItem in items:
		m = re.match(p,EachItem)
		if m is not None:
			return(m.group(1))
	return('NA')

# test: if used as main
if __name__=='__main__':
	import re
	import sys
	import shelve
	TransDB = shelve.open('class_GTF_shelve')
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
	TransDB.close()

	TransDB = shelve.open('class_GTF_shelve')
	t = TransDB['ENST00000456328']
	#print(t.TransID,t.GeneID,t.GeneType,t.Chromosome,t.Strand,sep='\t')
	for ix in range(t.ExonCount):
		print(ix,'=>',t.Exons[ix],sep='\t')
	print(t.getlength())
	print(t.getrelativeloc(12000))
	t = TransDB['ENST00000341832']
	#print(t.TransID,t.GeneID,t.GeneType,t.Chromosome,t.Strand,sep='\t')
	for ix in range(t.ExonCount):
		print(ix,'=>',t.Exons[ix],sep='\t')
	print(t.getlength())
	print(t.getrelativeloc(1655368))
	TransDB.close()
