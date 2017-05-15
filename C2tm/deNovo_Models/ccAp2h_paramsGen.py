# Marco Mravic DeGrado lab July 2016
# Generate a parameters file to build de novo D2 backbones
# python ccc3_ParamsGen.py ~/tertBuilding/MS1/params.txt

import sys, os, numpy as np

outFile = sys.argv[1]

# (chains, chL, r0, r1, w0, w1, a, ph1, cr, dph0, zoff, varargin)


### Variable Params

R_o 	= np.array( [3.8, 4, 4.2] )
W_o 	= np.array( [-3, -3.5, -4] )
Phi_1	= np.arange( 10, 110, 10 )
Z_AA	= np.array( [2, 2.5, 3, -2, -2.5, -3, -3.5] )

###

### Fixed params

chains		= '2'
chL 		= '25'
#r_o		VARIABLE
r_1			= '2.26'
phi_o		= '[180]'
topolopy 	= '[0]'
w_1			= 102.8

#N_alpha		= 3.6
#fix_w 		= 100.7

###

## Remaining parameters are calculated given the variable parameter

pSet = []
# (chains, chL, r0, r1, w0, w1, a, ph1, cr, dph0, zoff, varargin)
txt = '# (chains, chL, r0, r1, w0, w1, a, ph1, cr, dph0, zoff, varargin)\n'
for r_o in R_o:
	for phi1 in Phi_1:
		for w_o in W_o:
			for z_aa in Z_AA:
		

			## Caclulated parameters, only alpha remaining here

				N_super = 360/w_o # can also calculate by inverse of major/minor twist differential: 1/3.6 - (w_1/360)

				Pitch 	= -1 * ( (N_super * 1.51)**2 - 4 * ( np.pi**2 ) * ( r_o**2 ) )**0.5
				alpha_Pang	= round( 180* np.arctan( 2*np.pi*r_o / Pitch) / np.pi, 3)



				vals =  [ chains, chL, str( r_o ), str( r_1 ), str( w_o ), str( w_1 ), str(alpha_Pang), 
				'[%.1f, %.1f]' % ( phi1, phi1 ), topolopy, phi_o, str( z_aa ), '\'registerzoff\'',
					] 
				
				txt += ', '.join( vals ) + '\n'

				
#				print 360*( (1/ 3.6) - ( 1/ 3.5) )


outF = open( outFile, 'w' )
outF.write( txt )



