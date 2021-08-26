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
time docker run --rm -v `pwd`:`pwd` trinityrnaseq/trinityrnaseq \
    /usr/local/bin/trinityrnaseq/util/align_and_estimate_abundance.pl \
    --thread_count $threads \
    --transcripts `pwd`/$transcript \
    --seqType fq \
    --left  `pwd`/$left \
    --right `pwd`/$right \
    --est_method salmon \
    --salmon_add_opts "--validateMappings" \
    --prep_reference \
    --output_dir `pwd`/$outdir
