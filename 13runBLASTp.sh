#!/bin/sh
# exec BLAST
# name of query
query=E_ok.fasta
# name of blast program
blast=blastp
# E-value for threshold
evalue=1e-10
# threads to use
thre=24
#
gzip=pigz
#cd $workdir/phasmids_fa

for f in *.pep; do
  out=${query}_$f
  time $blast -query $query -db $f \
  -outfmt 6 \
  -max_target_seqs 1 \
  -evalue $evalue \
  -num_threads $thre \
  | $gzip -c \
  > $out.gz
done
