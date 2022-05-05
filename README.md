# SAQE
Systematic Analysis for Quantification of Everything (SAQE) is a set of scripts for quantification of transcripts using RNA-seq and metagenomic results.
SAQE consists of several scripts to do the analyses.
The number added in the name of script corresponds to the analysis bewlo.

- Expression (original SAQE(Systematic Analysis for Quantification of Expression))
    - 01 Retrieval of RNA-seq reads from the SRA database
    - 02 Conversion of data format and compression 
    - 03 Trimming and quality control of reads
    - 04 Transcriptome assembly by Trinity (skip if the transcriptome reference is available)
    - 05 Expression quantification by salmon ((direct) salmon or align_and_estimate_abundance.pl (AAEA) with salmon)
- Functional annotation (Fanflow) 
    - 11 Translating cDNA into protein sequence
    - 12 Getting reference protein sequences
    - 13 Making BLAST index
    - 14 Executing BLAST search (BLASTP)
    - 15 Executing global alignment search by ggsearch and extract needed information for further studies
    - 16 Getting Pfam and running HMMscan with parser for the functional annotation 
- Metagenome: see [`101Kraken2.md`](./101Kraken2.md) for details
    - 101 Building libarary Kraken2 for Kraken2
    - 102 Running Kraken2 for classification
    - 103 Visualizing multiple Kraken2 outputs for comparison 

## Requirements

- Miniconda is required to install `sra-tools`, `trim-galore` and `pigz`.
- Docker is also required to do the analyses in Trinity (04) and salmon (05). 
- Pitagora Workflows in Common Workflow Language (CWL) at https://github.com/pitagora-network/pitagora-cwl is required to run salmon script (05).

## How to cite these scripts?

Cite the paper below for the citation.

- For expression part:
> Bono H. Meta-Analysis of Oxidative Transcriptomes in Insects. *Antioxidants*. 2021; 10(3):345. [`https://doi.org/10.3390/antiox10030345`](https://doi.org/10.3390/antiox10030345)
- For functional annotation part: To be submitted.
- For metagenome part:
> Oec N & Bono H. Rapid metagenomic workflow using annotated 16S RNA dataset. *BioHackrXiv* [`https://doi.org/10.37044/osf.io/gbt8p`](https://doi.org/10.37044/osf.io/gbt8p)
