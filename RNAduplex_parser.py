# a parser for output of RNAduplex program
class RNAduplex:
	def __init__(self,Header1,Header2,Pairing):
		import re
		Header1 = Header1.replace('\n','')
		Header2 = Header2.replace('\n','')
		(self.ID1,self.Seq1) = Header1.split('_')
		(self.ID2,self.Seq2) = Header2.split('_')
		m = re.search('(^[.()]+)&([.()]+) +([0-9]+),([0-9]+) +: +([0-9]+),([0-9]+) +[(]{1} *([0-9+-.]+) *[)]{1}',Pairing)	
		self.Pairing1 = m.group(1)
		self.Pairing2 = m.group(2)
		self.Loc1 = [int(m.group(3)),int(m.group(4))]
		self.Loc2 = [int(m.group(5)),int(m.group(6))]
		self.Energy = m.group(7)

	def getpairing(self,pos,query='1st'):
		# input which strand you're asking and position
		# output [thispos,thisbase,thatpos,thatbase]
		if query=='1st':
			if pos<self.Loc1[0] or pos>self.Loc1[1]:
				return([pos,self.Seq1[pos-1],0,'Unp'])
			else:
				relpos = pos - self.Loc1[0]
				if self.Pairing1[relpos]=='.':
					return([pos,self.Seq1[pos-1],0,'Unp'])
				ixp = 0
				for ix in range(relpos+1):
					if self.Pairing1[ix]=='(':
						ixp+=1
				ixt = 0
				for ix in range(len(self.Pairing2))[::-1]:
					if self.Pairing2[ix]==')':
						ixt+=1
					if ixt == ixp:
						break
		#			print(ix,ixt,self.Pairing2[ix])
		#		print(relpos,ixp,ixt,ix)
				thatpos = self.Loc2[1] - (len(self.Pairing2)-ix) + 1 
				return([pos,self.Seq1[pos-1],thatpos,self.Seq2[thatpos-1]])

# test
if __name__ == '__main__':
	import sys
	InFile = open(sys.argv[1],'r')
	Lines = InFile.readlines()
	t = RNAduplex(Lines[0],Lines[1],Lines[2])
	print(t.Energy)
	print(t.getpairing(13))

					

