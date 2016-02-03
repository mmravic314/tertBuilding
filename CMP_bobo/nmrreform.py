from prody import *
import sys, os

inPDB = parsePDB( sys.argv[1] )

prvRes = 0
ch = ['A', 'B', 'C']
flag = 0

for c in inPDB.iterResidues():
	
	if c.getResnum() < prvRes:
		flag +=1

	if c.getResnum() > 80:
		c.setChids( 'D' )
		print c.getResnum(), c.getChids()
		continue
		
	c.setChids( ch[flag] )

	print c.getResnum(), c.getChids()

	prvRes = c.getResnum()
writePDB( sys.argv[1], inPDB )
