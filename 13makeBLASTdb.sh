#!/bin/sh
# makeBLASTdb
# specify directory for downloaded datasets
gzip=pigz
#dir=db 
#cd $dir
for fgz in *.pep.all.fa.gz; do
  $gzip -d $fgz
  f=`basename $fgz`
  g="${f%.gz}"
  makeblastdb -in $g -dbtype nucl -hash_index -parse_seqids
done
