#!/bin/sh
# exec ggsearch for global alignment
# name of query
query=query.fasta
# name of db
db=db.fasta
# threads to use
thre=4
# cutoff threshold (E-value)
evalue=0.1
# number of alignments
d=1
# name of program
ggsearch=ggsearch36
# outfile
out=ggsearch_${query}-${db}.txt
gzip=pigz
# run ggsearch
$ggsesarch -Q -T $thre -d $d -E $evalue $query $db \
| $gzip \
> $out
