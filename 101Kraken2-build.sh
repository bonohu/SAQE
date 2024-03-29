#!/bin/sh

# usage: 101Kraken2-build.sh DBNAME 
# 1. Set working directory 
DBNAME="/Users/bono/kraken2/"
#DBREFFASTA="16S_kraken2.fasta"
DBREFFASTA=$1 # should not compressed; ungzip FASTA
THREADS=14

# 2. Downloading required file(taxonomy and so on: `names.dmp` and `nodes.dmp`)
kraken2-build --download-taxonomy --db $DBNAME
#docker run -it -v `pwd`:/kk2 staphb/kraken2 kraken2-build --download-taxonomy --db /kk2/db

# 3. Installing reference library  
kraken2-build --add-to-library $DBREFFASTA --threads $THREADS --db $DBNAME
#docker run -it -v `pwd`:/kk2 staphb/kraken2 kraken2-build --add-to-library /kk2/$DBREFFASTA --threads $THREADS --db /kk2/db

# 4. Building database
kraken2-build --build --threads $THREADS --db $DBNAME
#docker run -it -v `pwd`:/kk2 staphb/kraken2 kraken2-build --build --threads $THREADS --db /kk2/db
