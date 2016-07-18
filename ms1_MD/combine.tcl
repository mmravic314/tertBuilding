#!/usr/local/bin/vmd
# join (parts of) protein complex with a membrane

# set echo on for debugging
echo on

# need psfgen module and topology
package require psfgen
topology ~/bin/toppar/top_all36_prot.rtf

# load structures
resetpsf
readpsf membrane.psf
coordpdb membrane.pdb
readpsf protein_only.psf
coordpdb protein_psfgen.pdb

# can delete some protein segments if needed
#set pseg2del   { "D" "E" "F" "G" "H" }
set pseg2del   { }
foreach seg $pseg2del {
  delatom $seg
}

# write temporary structure
set temp "temp"
writepsf $temp.psf
writepdb $temp.pdb

# reload full structure (do NOT resetpsf!)
mol load psf $temp.psf pdb $temp.pdb

# select and delete lipids that overlap protein:
# any atom to any atom distance under 0.8A
# (option: heavy atom to heavy atom distance under 1.3A)
set sellip [atomselect top "resname POPC"]
set lseglist [lsort -unique [$sellip get segid]]
foreach lseg $lseglist {
  # find lipid backbone atoms
  set selover [atomselect top "segid $lseg and within 0.8 of protein"]
  # delete these residues
  set resover [lsort -unique [$selover get resid]]
  foreach res $resover {
    delatom $lseg $res
  }
}
foreach res { } {delatom $LIP1 $res}
foreach res { } {delatom $LIP2 $res}

# select and delete waters that overlap protein:
set selwat [atomselect top "resname TIP3"]
set lseglist [lsort -unique [$selwat get segid]]
foreach lseg $lseglist {
  set selover [atomselect top "segid $lseg and within 3.8 of protein"]
  set resover [lsort -unique [$selover get resid]]
  foreach res $resover {
    delatom $lseg $res
  }
}
foreach res { } {delatom $WAT1 $res}
foreach res { } {delatom $WAT2 $res}

# write full structure
writepsf protein_and_membrane.psf
writepdb protein_and_membrane.pdb

# clean up
file delete $temp.psf
file delete $temp.pdb

# non-interactive script:   vmd -dispdev text < combine.tcl > combine.log
quit