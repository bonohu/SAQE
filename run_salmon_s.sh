#!/bin/sh
# number of threads to use
p=28
# workspace: Donwloads directory
githubdir=/Users/bono/Documents/github
#cd $github
# git clone pitagora-cwl
#git clone https://github.com/pitagora-network/pitagora-cwl
# retrieve reference transcriptome
#
# make salmon index
#cd /Users/bono/Documents/ioxidative
#cwltool $githubdir/pitagora-cwl/tools/salmon/index/salmon_index.cwl \
#--nthreads $p --index_name Human_gencode_salmon \
#--transcript_fasta gencode.v30.transcripts.fa.gz 
#salmonindex=Cel_salmon
salmonindex=Dme_salmon
# run salmon quant
#srrlist=fastq/SE/SRR_c.txt
srrlist=fastq/SE/SRR_d.txt
fqdir=fastq/SE/trim_galore

cd /Users/bono/Documents/ioxidative
for srr in `cat $srrlist`; do
  echo $srr
  time cwltool $githubdir/pitagora-cwl/tools/salmon/quant/single_end/salmon_quant_se.cwl \
  --fq $fqdir/${srr}.sra_trimmed.fq.gz \
  --index_dir $salmonindex --nthreads $p \
  --quant_out_dir salmon_out/${srr}_salmon_quant
done
