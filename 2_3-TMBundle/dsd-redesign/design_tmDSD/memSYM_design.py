# Marco Mravic DeGrado Lab May 2016

# First run symmetry creator 
# xray@dgl-xray:~/tertBuilding/2_3-TMBundle/dsd-redesign/design_tmDSD$ ~/rosetta/source/src/apps/public/symmetry/make_symmdef_file.pl -m NCS -a X -i Y -r 12.0 -p tmDSD_trimerBB.pdb > C3.symm



# input 1: pdb to input, oriented in the membrane.. auto grabs resfile and span file  
# input 2: protocol xml file
# input 3: path to rosetta 

# output: directory called 'designs' to store output files for design trajactories

## example command line
# xray@dgl-xray:~/tertBuilding/2_3-TMBundle/dsd-redesign/design_tmDSD$ python memSYM_design.py tmDSD_trimerBB_INPUT.pdb helix_DesignSYM.xml ~/rosetta/



import sys, os, subprocess as sp, time
start = time.time()

# I/O

inPdb 		= sys.argv[1]
inSpan		= inPdb[:-4] + '.span'
inXML		= sys.argv[2]
inResF		= os.path.join( os.path.dirname(inPdb), 'resfile' )

rosiBase 	= sys.argv[3]
rosiScrps	= os.path.join( rosiBase, 'source/bin/rosetta_scripts.linuxgccrelease' )
rosiSpanGen = os.path.join( rosiBase, 'source/bin/spanfile_from_pdb.linuxgccrelease')
rosiDB 		= os.path.join( rosiBase, 'database/' )

oDir 		= os.path.join( os.path.dirname(inPdb), 'outputs/' )

if not os.path.exists( oDir ):
	os.mkdir( oDir )



## Generate Span file (if not existing)... just hashed this out afte running once 
#if not os.path.exists( inSpan ):
cmdSpan = [ rosiSpanGen, 
		'-database', rosiDB, 
		'-in:file:s', inPdb
		]	

#sp.call( cmdSpan )
## 
#print inSpan
#sys.exit()

##### Design ####

n = '1'

cmd = [  rosiScrps, 
'-parser:protocol', inXML, 					# Path to Rosetta script (see above)
'-in:file:s', inPdb,						# Input PDB structure
'-nstruct', n, 								# Generate 1000 models
'-mp:setup:spanfiles', inSpan,				# Input spanfile
'-mp:scoring:hbond', 						# Turn on membrane hydrogen bonding
'-relax:jump_move', 'true', 				# Allow jumps to move during relax
'-out:prefix', oDir,
'-packing:resfile', inResF,
'-out:overwrite',
'-packing:pack_missing_sidechains', '0' ]

print 
print cmd
print 

sp.call( cmd )

print 
print 'Entire run took this many seconds:', time.time() - start

