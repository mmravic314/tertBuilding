#!/usr/bin/bash

#$ -S /usr/bin/python
#$ -l mem_free=1G
#$ -l arch=linux-x64
#$ -l netapp=1G
#$ -l h_rt=00:10:00
#$ -cwd
#$ -j y
#$ -o /netapp/home/mmravic/tertBuilding/2_3-TMBundle/3helix_TM/apDesign/rnd2_design/memFolding/logs
#$ -t 1-100

#
#

# This isn't right but it does something
#bash ../../qsub_highResRefine_memFolding.sh ../toRelax_mmCentroids.txt "python ../../rosiRelax_centFolded.py  ~/rosetta/ ../../tmBundle_Relax.xml ../../Relaxed_sc_apTM3hb.span" 

inx=1
# tasks start at 1, so {1,2,...50000}, {50001,...100000}
#taskID=$SGE_TASK_ID 			#CLUSTER
taskID=1						# LOCAL 
stop=$(( $taskID ))


while read -r line
	do 
			# stop and execute command when on the proper parameter set
			if [ $inx -eq $stop ]
			then
				modelPath=$line
				echo $modelPath
				$2 $modelPath $taskID
				break
			fi
			inx=$(( inx + 1))
		

done < $1
