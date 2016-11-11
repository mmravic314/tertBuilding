# input asn residue. and align amide of each to make inverse rotamer, draw a helical segment around the inverse rotamer asn
# 

import sys, os, numpy as np
from prody import *


scaffold  = parsePDB( sys.argv[2] )

targ 	= scaffold.select( 'segment P3' )
bb 		= targ.select( 'backbone' ) 
amide 	= targ.select( 'name CG ND2 OD1' )

#helix
helix 	= parsePDB( sys.argv[3] ).select( 'resnum 1 to 13 and (not element H)' ).copy() 
helixMob= helix.select( 'resnum 7 and (name CA C O N CB)' )
helix.setSegnames( [ 'P2' for x in helix.iterAtoms() ] )



rots = [ os.path.join( sys.argv[1], f ) for f in os.listdir( sys.argv[1] ) if f[-4:] == '.pdb' ]

for r in sorted( rots ):
	print r
	resi = parsePDB(r).select( 'not element H' )
	mobile = resi.select( 'name CG ND2 OD1' )
	target = resi.select( 'name CA C O N CB' )

	print calcRMSD( mobile, amide ), resi.select( 'ca' ).getCoords()
	tMat = superpose( mobile, amide )[1]
	print calcRMSD( mobile, amide ), resi.select( 'ca' ).getCoords(), '\namide aligned\n'


	print calcRMSD( helixMob, target ), helixMob.select( 'ca' ).getCoords()
	tMat = superpose( helixMob, target )[1]
	print calcRMSD( helixMob, target ), helixMob.select( 'ca' ).getCoords()
	print 
#	sys.exit()
	mobile.setResnums([ 7 for x in [ 'CA C O N CB'.split() ] ])
	newH = helix + mobile.copy()

	nPath = os.path.basename( r )[:-4] + '_h.pdb'
	writePDB(nPath, newH)
	
	# now write a 13 residue helical segment supporting the target ASN 
	


