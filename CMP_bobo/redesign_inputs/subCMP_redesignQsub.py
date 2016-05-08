#!/usr/bin/env python2.7

#$ -S /usr/bin/python
#$ -l mem_free=1G
#$ -l arch=linux-x64
#$ -l netapp=1G
#$ -l h_rt=00:05:00
#$ -cwd
#$ -j y
#$ -o /netapp/home/mmravic/tertBuilding/CMP_bobo/redesign_inputs/logs
#$ -t 1-20000

#############
# qsub subCMP_redesignQsub.py ~/bin/Rosetta/ loopFragStitch.pdb CMP_boboREDESIGN.xml CMP_bobo_trj_rnd2.resfile loopFragStitch.cst ~/tertBuilding/CMP_bobo/redesign_inputs/rnd2_outputs/
#############


### local design
# python subCMP_redesignQsub.py ~/rosetta/ ~/tertBuilding/CMP_bobo/redesign_inputs/loopFragStitch.pdb CMP_boboREDESIGN.xml CMP_bobo_trj3.resfile loopFragStitch.cst 
##

## local repack to get desing threshold
# xray@dgl-xray:~/tertBuilding/CMP_bobo/redesign_inputs$ python subCMP_redesignQsub.py ~/rosetta/ ~/tertBuilding/CMP_bobo/redesign_inputs/loopFragOG.pdb CMP_boboreapckOG.xml CMP_bobo_OG.resfile 
#


# 1) path 2 rosetta main
# 2) path to input structure file
# 3) path to XML script for protocol
# 4) resfile
# 5) constraint file for backbone atom minimization
import sys, os, subprocess as sp, re

#### INPUT NOTE: Due to author laziness,regex fails for '~/peptideAmyloid/rosettaFixBB/input1/' .... so leave this '/' out!!!

################## MAIN #######################
# Non-variable args
rosetta_database_path   = os.path.join( sys.argv[1] , 'database/' )
rosetta_scriptsEXE_path = os.path.join( sys.argv[1], 'source/bin/rosetta_scripts.linuxgccrelease' )
design_script_path      = sys.argv[3]
struc_path 				= sys.argv[2]
resfile_path			= sys.argv[4]
cst_path				= sys.argv[5]

# Variable args

output_prefix			= sys.argv[6]
try:
	output_suffix 			= '_out%s' % (str(  os.environ["SGE_TASK_ID"]) )
except KeyError:
	output_suffix                      = '_out%s' % ( 'Local' )

cmd = [
		rosetta_scriptsEXE_path,
		'-database', rosetta_database_path,
		'-parser:protocol', design_script_path,
		'-in:file:s', struc_path,
		'-out:prefix', output_prefix,   
		'-out:suffix', output_suffix,                               
		'-out:no_nstruct_label',
		'-out:overwrite',
		'-use_input_sc',
        '-packing:resfile', resfile_path,
		'-parser:script_vars', 'cst_file=%s' % ( cst_path )
]

print
print cmd
print

sp.call( cmd )
