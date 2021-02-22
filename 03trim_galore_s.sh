#!/bin/sh
threads=8
fqdir=../fq
mkdir trim_galore
cd trim_galore
# assumed fastq file in another directory, called $fqdir
for f in $fqdir/*.fastq.gz ; do
	time trim_galore -j $threads --gzip --fastqc --trim1 $f
done
