#!/bin/sh
fqdir=../fq # directory where fastq files are located
threads=8
mkdir trim_galore
cd trim_galore
for fq in $fqdir/*_1.fastq.gz; 
	do g="${fq%_1.fastq.gz}"
	echo $g
	time trim_galore -j $threads --gzip --fastqc --trim1 --paired ${g}_1.fastq.gz ${g}_2.fastq.gz
done
