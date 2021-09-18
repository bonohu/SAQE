#!/bin/sh

# 1. Set working directory 
FQ=$1
REPORTF="$FQ.rep.txt"
#THREADS=14

# 1. Classification & output
#kraken2 --db $DBNAME --gzip-compressed $FQ --threads $THREADS --report $REPORTF --output -
docker run -it --env KRAKEN2_DB_PATH=`pwd`/db -v `pwd`:/kk2 staphb/kraken2 kraken2 --db /kk2/db --gzip-compressed /kk2/$FQ --report /kk2/$REPORTF --output - 
 ```
