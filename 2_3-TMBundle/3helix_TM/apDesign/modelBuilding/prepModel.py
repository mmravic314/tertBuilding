import os, sys, numpy as np
from prody import * 

#  python prepModel.py coreHBclean.pdb ~/bin/40_allAlaIdealHelix.pdb
inPdb 	= parsePDB( sys.argv[1] )

#
helices = [ h.copy() for h in inPdb.iterSegments() ]

# load helix and clean it up
extH 	= parsePDB( sys.argv[2] )

# This is number of residues to extend... here symmetric and same in all directions
nExt = 8

#Do extension to each helix, and joing them into a new atom group

newPDB = ''
for s in helices:
	
	# learn helix length, chain and segment name
	ch 	= s.getChids()[0]
	seg = s.getSegnames()[0]
	try:
		hL = len( s.select( 'ca ' ) )
	except ValueError:
		print 'empty atom grup.... exiting'
		sys.exit()

	# first renumber
	n 	= nExt  # number to extend by is n-1

	for r in s.iterResidues():
		r.setResnum( n )
		n += 1


	# Now align C-terminal extension using a 7 residue alignment (variable), excluding terminal residue of target fragment
	alignLen = 7
	cRng 	= ' '.join( [ str(x) for x in np.arange( nExt + 1,  nExt + 1 + alignLen ) ] )
	mobile 	= extH.select( 'bb resnum %s' % cRng ).copy()
	target 	= s.select( 'bb resnum %s' % cRng )

	tMat 	= calcTransformation( mobile, target )

	cExtRng = ' '.join( [ str(x) for x in np.arange( 1,  nExt + 2 ) ] )
	draggC	= extH.select( 'resnum  %s' % cExtRng ).copy()
	draggC 	= applyTransformation( tMat, draggC )


	#Do the same alignment for the N-terminal extension
	strAlign, strResi , endResi = nExt + hL - alignLen - 1, nExt + hL - 1, nExt + hL + nExt - 1   # 20, 

	nRng 	= ' '.join( [ str(x) for x in np.arange( strAlign,  strAlign + alignLen ) ] )
	mobile 	= extH.select( 'bb resnum %s' % nRng ).copy()
	target 	= s.select( 'bb resnum %s' % nRng )

	tMat 	= calcTransformation( mobile, target )

	nExtRng = ' '.join( [ str(x) for x in np.arange( strResi,  endResi + 1 ) ] )
	draggN = extH.select( 'resnum  %s' % nExtRng ).copy()
	draggN = applyTransformation( tMat, draggN )

	# Clean up the transformed helical fragments and join to the target input helix... REMOVE THE C & N termini FROM the target **
	draggC.setSegnames( [ seg for x in draggC.iterAtoms()] )
	draggC.setChids( [ ch for x in draggC.iterAtoms()] )
	draggN.setSegnames( [ seg for x in draggN.iterAtoms()] )
	draggN.setChids( [ ch for x in draggN.iterAtoms()] )



	# redefining the overloaded varibale target, as final segment that alignment was done on
	targRng = ' '.join( [ str(x) for x in np.arange( nExt + 2, n - 1 )  ] )
	target	= s.select( 'resnum %s' % targRng).copy()


	# Put the fragments together to make a PDB together
	if len(newPDB) == 0:
		newPDB = draggC + target + draggN
		print 'here!!'
	else:
		newPDB = newPDB + draggC + target + draggN

	writePDB( 'tmp.pdb', newPDB )

