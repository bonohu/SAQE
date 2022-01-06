#!/bin/sh
# HMMscan: scan Pfam HMM 
# query in protein sequence
query=hoge.fasta
# threads to use
thre=4
# E-value threshold
evalue=1e-10
gzip=pigz
# Retrieve Pfam-A.hmm.gz
curl -O ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz
# Uncompress the file retrieved
$gzip -d Pfam-A.hmm.gz
# Make index
hmmpress Pfam-A.hmm
# Running hmmscan
% hmmscan -o hmmscan-${query}.txt --cpu $thre -E $evalue Pfam-A.hmm $query
