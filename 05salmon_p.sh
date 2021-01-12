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
salmonindex=Cel_salmon
# run salmon quant
#SRR3173746.sra_2_val_2.fq.gz
#srrlist=fastq/PE/SRR.txt
srrlist=ERR.txt
cd /Users/bono/Documents/ioxidative
fqdir=fastq/PE/trim_galore
for srr in `cat $srrlist`; do
  echo $srr
  time cwltool $githubdir/pitagora-cwl/tools/salmon/quant/paired_end/salmon_quant_pe.cwl \
  --fq1 $fqdir/${srr}.sra_1_val_1.fq.gz --fq2 $fqdir/${srr}.sra_2_val_2.fq.gz \
  --index_dir $salmonindex --nthreads $p \
  --quant_out_dir salmon_out/${srr}_salmon_quant
done
