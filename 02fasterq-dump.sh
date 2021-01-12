#!/bin/sh
# SRA files retrieved by prefetch reside at ~/ncb/public/ directory

for f in ~/ncbi/public/*.sra; do
 echo $f
 time fasterq-dump $f
done
