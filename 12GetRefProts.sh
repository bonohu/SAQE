#!/bin/sh
# GetRefs: download reference protein datasets
# specify directory for downloaded datasets
dir=db 
#
cd $dir
# human
curl -O https://ftp.ensembl.org/pub/current_fasta/homo_sapiens/pep/Homo_sapiens.GRCh38.pep.all.fa.gz
# mouse
curl -O https://ftp.ensembl.org/pub/current_fasta/mus_musculus/pep/Mus_musculus.GRCm39.pep.all.fa.gz
# fly
curl -O https://ftp.ensembl.org/pub/current_fasta/drosophila_melanogaster/pep/Drosophila_melanogaster.BDGP6.32.pep.all.fa.gz
# worm
curl -O https://ftp.ensembl.org/pub/current_fasta/caenorhabditis_elegans/pep/Caenorhabditis_elegans.WBcel235.pep.all.fa.gz
