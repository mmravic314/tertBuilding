# Marco Mravic DeGrado lab ucsf May 2017
# input a directory of pdb files
# extract tightest interacting 12 residue subset of a 2 helix dimer, print to file

# python extract_tight12Interface.py ./

import sys, os, numpy as np
from collections import defaultdict
from prody import *

dirPath 	= sys.argv[1]
helixSize 	= 12

elements 	= { 'N':'N', 'CA':'C', 'C':'C', 'O':"O", 'H':'H' }

for f in os.listdir( dirPath ):
	if f[:4] == 'mini' or f[-3:] != 'pdb': continue			# skip output files and non-pdb

	# first clean up fiele naming from online CCCP... also delete file if absval( ZoffAA ) < 2 
	fPath 		= os.path.join( dirPath, f )
	skip_flag 	= 0
	with open( fPath ) as fin:
		line = fin.readline()
		if np.fabs( float( line.split()[-1] ) ) < 2: 
			skip_flag += 1

	if skip_flag: continue
#	print np.fabs( float( line.split()[-1] ) )

	pdb 	= parsePDB( fPath )

	for a in pdb.iterAtoms():
		a.setElement( elements[a.getName()] ) 

	helix_A = pdb.select('ca chain A ')
	helix_B = pdb.select('ca chain B ')

	dstMtrx = buildDistMatrix( helix_A, helix_B)
	stp =0
	distList = []

	# calculate the mean inverse distance for each subwindow
	stop 	= len( dstMtrx.T ) - helixSize
	maxVal, indx  = -100, 0
	for j in dstMtrx.T:

		if stp == stop + 1: 
				break

		meanInvDist = np.mean( 1 / dstMtrx.T[stp:stp + helixSize,:] )

		if meanInvDist >  maxVal:
			maxVal = meanInvDist
			indx = stp
		stp +=1


	mini_pdb = pdb.select( 'chain A resnum %d to %d' % (indx, indx + helixSize - 1) ) + pdb.select( 'chain B resnum %d to %d' % (indx, indx + helixSize - 1) ) 
	mini_pdb.setTitle( line )
	newPath  = os.path.join( dirPath, 'mini_' + f )
	writePDB( newPath, mini_pdb ) 

