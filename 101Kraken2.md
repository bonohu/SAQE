# Metagenome data analysis workflow by Kraken2 

## Download annotated FASTA for Kraken2

Annotated FASTA file for Kraken2 (`16S_kraken2.fasta`) is proved by [Life Science Database Archive](https://dbarchive.biosciencedbc.jp/index-e.html) at JST [National Bioscience Database Center (NBDC)](https://biosciencedbc.jp/en/).
Please download from [the download site of 16S RNA sequence set for metagenomic analysis](https://dbarchive.biosciencedbc.jp/en/metagenomerefdb/download.html).

## Building library 

### 1. Set working directory
```
    $ DBNAME="/home/{yourname}/kraken2/"
```

### 2. Downloading required file(taxonomy and so on: `names.dmp` and `nodes.dmp`)
```
    $ kraken2-build --download-taxonomy --db $DBNAME
```

#### Docker version
`kk2` is the name of kraken2 directory in Docker environment.

```
    $ docker run -it -v `pwd`:/kk2 staphb/kraken2 kraken2-build --download-taxonomy --db /kk2/db
```

### 3. Installing reference library  

```
    $ kraken2-build --add-to-library 16S_kraken2.fasta --threads {n} --db $DBNAME
```

#### Docker version
```
    $ docker run -it -v `pwd`:/kk2 staphb/kraken2 kraken2-build --add-to-library /kk2/16S_kraken2_db_2021_5b.fasta --threads 14 --db /kk2/db
```

You may see error message for `dustmasker`. We now ignore this error.
> Masking low-complexity regions of new file...Unable to find dustmasker in path, can't mask low-complexity sequences

### 4. Building database
Specify {n} for the number of threads to use.

```
    $ kraken2-build --build --threads {n}  --db $DBNAME
```

#### Docker version
```
    $ docker run -it -v `pwd`:/kk2 staphb/kraken2 kraken2-build --build --threads {n} --db /kk2/db
```


## Classification & Visualization

### 1. run kraken2

FASTQ file (`sample1.fq.gz`) in `fq` directory.
The classification report will be written to `report.txt`.

```
    $ kraken2 --db $DBNAME --gzip-compressed fq/sample1.fq.gz --threads {n} --report report.txt --output -
```

#### Docker version

```
    $ docker run -it --env KRAKEN2_DB_PATH=`pwd`/db -v `pwd`:/kk2 staphb/kraken2 kraken2 --db /kk2/db --gzip-compressed /kk2/fq/sample1.fq.gz --report /kk2/F2s.txt --output - 
 ```

### 2. visualization

This part is not included in shell script because multiple results can be included and compared in this visualization.
So, run the commands below separately.

```
$ pip install jinja2 pandas
$ python karaken2_report_formatter.py -n sample_name_1 sample_name_2 -f sample_report_1 sample_report_2
```
