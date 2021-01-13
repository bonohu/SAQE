#!/bin/sh
# run Trinity using Docker
# for multiple files, the simplest way is to cat these files.
left=sample_1.fq.gz
right=sample_2.fq.gz
memory=128G
cpu=28
outdir=trinity_out_dir
#
time docker run --rm -v `pwd`:`pwd` trinityrnaseq/trinityrnaseq Trinity \
  --seqType fq \
  --left `pwd`/$left \
  --right `pwd`/$right \
  --max_memory $memory --CPU $cpu --output `pwd`/$outdir
