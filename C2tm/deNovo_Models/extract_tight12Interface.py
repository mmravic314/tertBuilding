# Marco Mravic DeGrado lab ucsf May 2017
# input a directory of pdb files
# extract tightest interacting 12 residue subset of a 2 helix dimer, print to file

# python extract_tight12Interface.py ./

import sys, os, numpy as np
from collections import defaultdict
from prody import *

dirPath 	= sys.argv[1]
helixSize 	= 12

for f in os.listdir( dirPath ):
	if f[:4] == 'mini' or f[-3:] != 'pdb': continue			# skip output files and non-pdb

	fPath 	= os.path.join( dirPath, f )
	pdb 	= parsePDB( fPath )

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
			indx = stp
		stp +=1

	mini_pdb = pdb.select( 'resnum %d to %d' % (indx, indx + helixSize - 1) ) 
	newPath  = os.path.join( dirPath, 'mini_' + f )
	writePDB( newPath, mini_pdb ) 

