# read in a 2 column match | pdb file, then print out file with columns of coiled-coil parameters

import sys, os, numpy as np 

def parseHeader( text ):
	line 	= text.split()
	Ro 		= str( float( line[9][:-1] ) )
	wo 		= str( float( line[15][:-1] ) )
	phi1 	= str( float( line[25][:-2] ) )
	Zaa 	= str( float( line[-1] ) )
	data = [ Ro, wo,  phi1, Zaa  ]


	return ' '.join( data )

txt = '#Varied: Ro wo phi1 Zaa | fixed: w1=102.85 phi_o=180 R1=2.26 Pitch-coupled \n'
with open( sys.argv[1] ) as fin:
	for i in fin:
		line = i.split()
		headPath = os.path.join( sys.argv[2], line[1][5:-3] + 'pdb' )
		with open( headPath ) as f:
			header = f.readline()

		txt += '%s %s %s\n' % ( line[0], headPath, parseHeader( header ) )

outFile = sys.argv[1][:-4] + '_params.txt'
oF = open( outFile , 'w')
oF.write( txt )  
