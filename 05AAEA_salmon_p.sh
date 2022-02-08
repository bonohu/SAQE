#!/bin/sh
# run align_and_estimate_abundance.pl (AAEA) in Trinity with salmon using Docker
# for multiple files, the simplest way is to cat these files.
left=sample_1.fq.gz
right=sample_2.fq.gz
memory=128G
threads=28
transcript=trinity_out_dir/Trinity.fasta #name of transcript
outdir=salmon_out
#
time docker run --rm -v `pwd`:`pwd` trinityrnaseq/trinityrnaseq:2.11.0 \
    /usr/local/bin/trinityrnaseq/util/align_and_estimate_abundance.pl \
    --thread_count $threads \
    --transcripts `pwd`/$transcript \
    --trinity_mode \
    --seqType fq \
    --left  `pwd`/$left \
    --right `pwd`/$right \
    --est_method salmon \
    --prep_reference \
    --output_dir `pwd`/$outdir
