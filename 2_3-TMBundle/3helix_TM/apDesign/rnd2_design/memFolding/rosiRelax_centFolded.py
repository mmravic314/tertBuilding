#!/usr/bin/python
import sys, os, subprocess as sp, time
start = time.time()

# I/O

inPdb 		= sys.argv[4]
inSpan		= sys.argv[3]
inXML		= sys.argv[2]

rosiBase 	= sys.argv[1]
rosiScrps	= os.path.join( rosiBase, 'source/bin/rosetta_scripts.linuxgccrelease' )
rosiDB 		= os.path.join( rosiBase, 'database/' )

taskIDmod  	= '_' + sys.argv[5]


# a hole for the annoying stdout to crawl in and decay
FNULL = open(os.devnull, 'w')

#if not os.path.exists( oDir ):
#	os.mkdir( oDir )


n = '1'

cmd = [  rosiScrps, 
'-database', rosiDB,
'-parser:protocol', inXML, 					# Path to Rosetta script (see above)
'-in:file:s', inPdb,						# Input PDB structure
'-nstruct', n, 								# Generate 1000 models
'-mp:setup:spanfiles', inSpan,				# Input spanfile
'-mp:scoring:hbond', 						# Turn on membrane hydrogen bonding
'-relax:jump_move', 'true', 				# Allow jumps to move during relax
#'-out:prefix', oDir,
#'-relax:fast', 
'-out:overwrite',
'-out:suffix', taskIDmod,
'-packing:pack_missing_sidechains', '0', 
'-ignore_zero_occupancy', 'false']

cmd = " ".join( cmd )

print 
print cmd
print 
print sys.argv
print

#sp.call( cmd, stdout=FNULL, stderr=sp.STDOUT )
sp.call( cmd, shell=True )


print 
print 'Entire run took this many seconds:', time.time() - start