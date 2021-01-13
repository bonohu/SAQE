#!/bin/sh
# run Trinity using Docker
# for multiple files, the simplest way is to cat these files.
left=sample_1.fq.gz
right=sample_2.fq.gz
memory=128G
threads=12
outdir=trinity_out_dir
#
time docker run -v`pwd`:`pwd` trinityrnaseq/trinityrnaseq \
 /usr/local/bin/trinityrnaseq/util/align_and_estimate_abundance.pl \
 --thread_count $threads \
 --transcripts $transcript \
 --seqType fq \
 --left  $left \
 --right $right \
 --est_method salmon \
 --salmon_idx_type quasi \
 --salmon_add_opts "-p $threads" \
 --prep_reference --output_dir salmon_out

