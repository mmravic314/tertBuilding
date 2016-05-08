#!/usr/bin/python

#$ -S /usr/bin/python
#$ -l mem_free=1G
#$ -l arch=linux-x64
#$ -l netapp=1G
#$ -l h_rt=00:10:00
#$ -cwd
#$ -j y
#$ -o /netapp/home/mmravic/tertBuilding/CMP_bobo/folding/logs
#$ -t 1-5

# Rosetta ab initio folding

# input 1: path to rosetta
# input 2: path to fasta file with single sequence to fold
# input 3: path to working dir, should have frag_3 and frag_9 files
# input 4: path to secondary structure prediction .psipred_ss2 file (from Robetta frag maker)

# Example command line (Local)
#  python ~/tertBuilding/CMP_bobo/folding/bin/rosi_refold_local.py ~/rosetta/ ~/tertBuilding/CMP_bobo/folding/21169/model_21169.fasta ~/tertBuilding/CMP_bobo/folding/21169/ ~/tertBuilding/CMP_bobo/folding/21169/21169.psipred_ss2

# EXAMPLE QSUB
# qsub ~/tertBuilding/CMP_bobo/folding/bin/rosi_refold_local.py ~/bin/Rosetta/ ~/tertBuilding/CMP_bobo/folding/21169/model_21169.fasta ~/tertBuilding/CMP_bobo/folding/21169/ ~/tertBuilding/CMP_bobo/folding/21169/21169.psipred_ss2




import sys, os, subprocess as sp, time

start = time.time()


## I/O 

rosiDB 		= os.path.join( sys.argv[1], 'database/' )
rosiFOLD	= os.path.join( sys.argv[1], 'source/bin/AbinitioRelax.linuxgccrelease' ) 
rosiSCORE	= os.path.join( sys.argv[1], 'source/bin/score.linuxgccrelease' )

inFasta 	= sys.argv[2]

wrkDir 		= sys.argv[3]
outputs 	= os.path.join( wrkDir, 'output/' )

if not os.path.exists( outputs ):
	os.mkdir( outputs )

frag_3 		= os.path.join( wrkDir, 'frag_3' )
frag_9 		= os.path.join( wrkDir, 'frag_9' )

modelTag 	= 'model_' + os.path.basename( wrkDir[:-1] )
ss2F 		= sys.argv[4]



add_nulls = lambda number, zero_count : "{0:0{1}d}".format(number, zero_count)
try:
	output_suffix 			= add_nulls( os.environ["SGE_TASK_ID"], 7 ) 
except KeyError:
	output_suffix                      = add_nulls( 1, 7 )

outF 	= modelTag + '_%s.pdb' % output_suffix 
sil_out = os.path.join( outputs, modelTag + '_%s.out' % output_suffix )

###






cmd = [ rosiFOLD, 
'-database', 				rosiDB, 
'-in:file:fasta', 			inFasta,
'-in:file:frag3', 			frag_3,
'-in:file:frag9', 			frag_9,
'-abinitio:relax', 			'True',
'-abinitio::increase_cycles', '10',
'-abinitio::rg_reweight', 	'0.5',
'-abinitio::rsd_wt_helix', 	'0.5',
'-abinitio::rsd_wt_loop', 	'0.5',
'-use_filters', 			'true', 
'-nstruct',					 '1',
'-out:overwrite', 
'-out:file:silent', 		sil_out,
'-psipred_ss2',				ss2F,
'-constant_seed'
]


print  '\n', cmd, '\n'
# Run design
sp.call( cmd )




print 
print 'time elapsed (s)', time.time() - start  
print 


sys.exit()


scCMD = [ rosiSCORE, 
'-database', rosiDB, 
'-in:file:silent', sil_out,

'-out:path:pdb', outputs, 
#'-out:prefix', outputs, 
'-out:output'

]
print scCMD 
print

sp.call( scCMD )

print 
print scCMD 
print


'''

        -database ../../rosetta_database \
        -in:file:fasta ./input_files/1elwA.fasta \
        -in:file:native ./input_files/1elw.pdb \
        -in:file:frag3 ./input_files/aa1elwA03_05.200_v1_3 \
        -in:file:frag9 ./input_files/aa1elwA09_05.200_v1_3 \
        -abinitio:relax \
        -relax:fast \
        -abinitio::increase_cycles 10 \
        -abinitio::rg_reweight 0.5 \
        -abinitio::rsd_wt_helix 0.5 \
        -abinitio::rsd_wt_loop 0.5 \
        -use_filters true \
        -psipred_ss2 ./input_files/1elwA.psipred_ss2 \
        -kill_hairpins ./input_files/1elwA.psipred_ss2 \
	-out:file:silent 1elwA_silent.out \
        -nstruct 10

'''