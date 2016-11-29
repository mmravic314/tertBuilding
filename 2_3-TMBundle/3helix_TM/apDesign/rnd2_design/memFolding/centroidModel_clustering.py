# Marco Mravic DeGrado Lab Nov 2016

#  structural clustering with mini-batch hierarchical clustering with a RMSD(radius) dependednt dyanmic k-mediods
# Take 400 decoys, and do a hierachical clustering with a clustering radius of 2 to set cluster number. 
# From the mini-batch, pick centroids and place remaining structures into each cluster.
# if any structure is further than the clustering radius, initialize a new cluster with this struct as centroid.

#
# python ../centroidModel_clustering.py outputsQsub/ ../Relaxed_sc_apTM3hb.span dMat_MiniBatch.pkl > ../LowResFolding_Clusters.txt 
#
#


from prody import *
import sys, os, numpy as np, cPickle as pic
from collections import defaultdict

inDir 			= sys.argv[1]
inSpan 			= sys.argv[2]
pklminiBatch 	= sys.argv[3]


############# FUNCTIONS ##############################

def miniBatch_Hierachical( pathList ):

	# do all non-redundant and non-idential comparisons between elements in the array, by noting & skipping redundants 
	reached, r , c, dMat = [], 0 , 0, np.zeros( (len(pathList),len(pathList)) )
	for a in pathList:
		c =0
		target = parsePDB( a ).select( selStr )

		for b in pathList:
#			print a, b, r, c,

			if b in reached or a==b: 
				c +=1
#				print
				continue
			
			mobile = parsePDB( b ).select( selStr )
			superpose( mobile, target )
			rmsd = round(calcRMSD( mobile, target ), 1 )
#			print rmsd
			dMat[r][c] = rmsd
			dMat[c][r] = rmsd

			c+=1
		reached.append(a)
		r +=1


	return dMat


############# FUNCTIONS END ##########################




################# MAIN ###################


# Get tm regions from span
selStr 	= []
flg 	= 0
with open( inSpan ) as fin:
	for i in fin:


		if i.strip() == 'n2c':
			flg+=1

		elif flg:
			a,b = tuple(  i.split() )
			selStr.append( '%s to %s' % ( a,b ) )
		else: 
			continue
selStr = 'ca resnum ' + ' '.join( selStr )

stp 	 = 0
pathList = []
miniSize = 400
fullList = []
for f in os.listdir( inDir ):

		path = os.path.join( inDir, f )
		# ignore empty files 
		size = os.stat(path).st_size
		if f[-4:] != '.pdb' or size ==0:
			continue
		elif stp < miniSize: 
			pathList.append( path )
#			print path, stp
		fullList.append( path )
		stp +=1


import scipy.spatial.distance as ssd
from scipy.cluster.hierarchy import linkage, fcluster
# Now look throught the files, collect the first 400 and create a pariwise RMSD... can save this to pkl, to do only once

if not os.path.exists( pklminiBatch ):


	dMat 		= miniBatch_Hierachical( pathList )
	pic.dump( dMat, open( pklminiBatch, 'wb' ) )
else:
	dMat 		= pic.load( open( pklminiBatch, 'rb' ) )


distArray 	= ssd.squareform( dMat )
# Clustering cutoff 4
cutoff 	  	= 4.  

print 'complete linkage clustering, cutoff =', cutoff
# perform complete linkage clustering & return clusters at described cutoff
linkMat 	= linkage( distArray, method='complete', metric='euclidean')
clust 		= fcluster( linkMat, cutoff, criterion='distance')
numClust 	= len( set(clust) )
print 'Unique clusters found:', numClust, '\n'		## This was 49 at 4.0 angstrom RMSD, batch size = 400

# Try to find cluster centroids by doing 100 iterations of k-medioids with randomly selected members as heads of each cluster
from Bio.Cluster.cluster import kmedoids
	
clusts, cost,num	= kmedoids( distArray, nclusters=numClust, npass=200)

#stp, initClust, recall = 0, [], {}
#for k in clust:
#	if k not in recall.keys():
#		initClust.append( stp )
#		recall[k]=stp
#		stp +=1
#	else:
#		initClust.append( recall[k] )

# convert clustering to a key to the centroids, print to file, and load each pdb with ProDy 
atomGroups 	= {}
clustTxt 	= ''
for k in sorted( set( clusts ) ):
#	print k-1, pathList[k-1]
	clustTxt += '%s %s \n' % ( pathList[k-1], k-1 )
	atomGroups[ pathList[k-1] ] = parsePDB( pathList[k-1] ).select( selStr )
oF = open('clustermedoids.txt','w')
oF.write(clustTxt)
oF.close()

# Try clustering the first 
keys = sorted( atomGroups.keys() )

clusters = defaultdict(list)
import time
stp, start = 0, time.time()
for m in fullList:

	rmsd = []
	mobile = parsePDB( m ).select( selStr )
	
	for cent in keys:
		tmp 	= mobile.copy()
		target 	= atomGroups[cent]
		superpose( tmp, target )
		rmsd.append( calcRMSD( tmp, target )  )
	#	print cent, calcRMSD( tmp, target )


	minR 	= np.min( rmsd )
#	print m, minR
	# If model is reached with radius > 4 Ang from an existing model, make a new cluster & load the PDB into memory
	if minR > 4.6:
		atomGroups[m] = mobile
		keys.append(m)
		clusters[ m ].append( ( minR, m ) )
		print 'made new cluster', m, round( minR, 2)
	# otherwise, assign to an existing cluster
	else:
		#print keys[rmsd.index( minR )]
		clusters[ keys[rmsd.index( minR )] ].append( ( minR, m ) )


	stp += 1
#	if stp > 500: break

print 'time elapsed (s)', time.time() - start, 'to process %d models' % stp

stp = 1
for k, v in clusters.items():
	print '>clust %d centroid:' % stp, k, len(v)
	for c in v:
		print round( c[0], 2), c[1]
	print
	stp += 1