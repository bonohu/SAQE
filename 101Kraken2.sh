#!/bin/sh

# 1. Set working directory 
FQ=$1
DBNAME="/Users/bono/kraken2/"
DBREFFASTA="16S_kraken2.fasta"
THREADS=14
REPORTF="$FQ.rep.txt"

# 2. Downloading required file(taxonomy and so on: `names.dmp` and `nodes.dmp`)
#kraken2-build --download-taxonomy --db $DBNAME
docker run -it -v `pwd`:/kk2 staphb/kraken2 kraken2-build --download-taxonomy --db /kk2/db

# 3. Installing reference library  
#kraken2-build --add-to-library 16S_kraken2.fasta --threads {n} --db $DBNAME
docker run -it -v `pwd`:/kk2 staphb/kraken2 kraken2-build --add-to-library /kk2/$DBREFFASTA --threads $THREADS --db /kk2/db

# 4. Building database
#kraken2-build --build --threads $THREADS --db $DBNAME
docker run -it -v `pwd`:/kk2 staphb/kraken2 kraken2-build --build --threads $THREADS --db /kk2/db

# 5. Classification & output
#kraken2 --db $DBNAME --gzip-compressed $FQ --threads $THREADS --report $REPORTF --output -
docker run -it --env KRAKEN2_DB_PATH=`pwd`/db -v `pwd`:/kk2 staphb/kraken2 kraken2 --db /kk2/db --gzip-compressed /kk2/$FQ --report /kk2/$REPORTF --output - 
 ```
