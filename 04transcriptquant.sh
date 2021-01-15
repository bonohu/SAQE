#!/bin/sh
# run Trinity using Docker
# for multiple files, the simplest way is to cat these files.

# usage: sh 04transcriptquant.sh midgut1
# name of sample from argument (example: midgut1)
sample=$1
# location of input files
transcript=`pwd`/trinity_out_dir/Trinity.fasta
left=`pwd`/trim_galore/${sample}_1_val_1.fq.gz
right=`pwd`/trim_galore/${sample}_2_val_2.fq.gz
memory=128G
threads=12
outdir=`pwd`/salmon_$sample
#
time docker run -v`pwd`:`pwd` trinityrnaseq/trinityrnaseq \
 /usr/local/bin/trinityrnaseq/util/align_and_estimate_abundance.pl \
 --thread_count $threads \
 --transcripts $transcript \
 --seqType fq \
 --left  $left \
 --right $right \
 --est_method salmon \
 --salmon_add_opts "-p $threads" \
 --prep_reference --output_dir $outdir
