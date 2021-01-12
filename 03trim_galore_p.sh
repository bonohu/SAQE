#!/bin/sh
fqdir=../fq # directory where fastq files are located
mkdir trim_galore
cd trim_galore
for fq in $fqdir/*_1.fastq; 
	do g="${fq%_1.fastq}"
	echo $g
	time trim_galore -j 8 --gzip --fastqc --trim1 --paired $fqdir/${g}_1.fastq $fqdir/${g}_2.fastq
done
