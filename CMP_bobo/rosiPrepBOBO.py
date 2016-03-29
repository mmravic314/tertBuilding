import sys, os

# write constraint file given fixed backbone for atoms not in the stitched region
loop 	= [8,9,10,11]
anchor 	= [4,5,6,7,12,13,14,15]
backbone= ['CA', 'O', 'C', 'N']
cst_txt = ''
first = 0
with open( sys.argv[1]) as file:
	for i in file:
		if i[:4] != 'ATOM': continue

		resnum 	= int( i[22:26].strip() )
		name 	= i[12:16].strip()

		# let Hydrogens and side chains free (unconstrained), especially since will be converted to Ala later
		if 'H' in name or name not in backbone: continue

		x, y, z = float( i[30:38] ), float( i[38:46] ), float( i[46:54] )

		if first == 0:
			cst_txt += 'CoordinateConstraint %s %d CA 18 %f %f %f HARMONIC 0.0 0.3\n' % ( name, resnum, x,y,z  )
			first += 1
			continue

		# lightly constraint CA's in the loop
		if resnum in loop:
			if name == 'CA':
				cst_txt += 'CoordinateConstraint %s %d N 1 %f %f %f HARMONIC 0.0 0.67\n' % ( name, resnum, x,y,z  )
				continue
			else:
				continue

		# do not constrain backbone positions
		if resnum in anchor:
			continue

		# constrain helix CA positions competely in ungraphed regions
		if name == 'CA':
			cst_txt += 'CoordinateConstraint %s %d N 1 %f %f %f HARMONIC 0.0 0.3\n' % ( name, resnum, x,y,z  )
			continue
		# looser restraint on all non-anchored positions
		cst_txt += 'CoordinateConstraint %s %d N 1 %f %f %f HARMONIC 0.0 0.8' % ( name, resnum, x,y,z  )

print cst_txt