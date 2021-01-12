#!/bin/sh
tmp=/tmp
mkdir trim_galore
cd trim_galore
# assumed fastq file in another directory, called 'fq'
for f in ../fq/*.fastq ; do
        trim_galore --fastqc --trim1 $f
done
