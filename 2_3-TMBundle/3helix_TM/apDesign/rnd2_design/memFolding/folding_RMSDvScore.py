# Marco Mravic DeGrado Lab Nov 2016
# Use this to align a directory full of rosetta membrane ab initio (low-res centroid) structures (folding trial) to some input model
# Default is C-alphas and only the TM regions from span file, but can change to backbone or full protein

# May also lead into structural clustering with mini-batch k-means

from prody import *
import sys, os, numpy as np

inDir 	= sys.argv[1]
inPDB 	= parsePDB( sys.argv[2], subset='ca' )
inSpan 	= sys.argv[3]

# Get tm regions from span
selStr 	= []
flg 	= 0
with open( inSpan ) as fin:
	for i in fin:


		if i.strip() == 'n2c':
			flg+=1

		elif flg:
			a,b = tuple(  i.split() )
			selStr.append( '%s to %s' % ( a,b ) )
		else: 
			continue
selStr = 'resnum ' + ' '.join( selStr )

target = inPDB.select( selStr )

# Now look throught the files, to parse score and align
score, rmsd = [], []
print 'Aligning pdbs from', inDir, 'to', sys.argv[1]

for f in os.listdir( inDir ):
	path = os.path.join( inDir, f )

	# find score
	with open( path ) as fin:
		for i in fin:
			if i[:4] == 'pose':
				score = float( i.rsplit()[-1] ) 

	# calculate best alignment of TM domains
	pdb 	= parsePDB( path, subset='ca' )
	mobile	= pdb.select( selStr )
	superpose( mobile, target )
	rmsd = calcRMSD( mobile, target )

	print f, score, rmsd

