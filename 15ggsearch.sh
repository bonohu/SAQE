#!/bin/sh
# exec ggsearch for global alignment
# name of query
query=$1
# name of db
db=$2
# threads to use
thre=8
# cutoff threshold (E-value)
evalue=0.1
# number of alignments
d=1
# name of program
ggsearch=ggsearch36
# outfile
out=ggsearch_${query}-${db}.txt.gz
gzip=pigz
# run ggsearch
time $ggsearch -Q -T $thre -d $d -m10 -E $evalue $query $db \
| $gzip \
> $out
