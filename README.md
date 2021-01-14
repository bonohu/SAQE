# SAQE
Systematic Analysis for Quantification of Expression (SAQE) is a set of scripts for quantification of transcripts using RNA-seq.
SAQE consists of several scripts to do the analyses.
The number added in the name of script corresponds to the analysis bewlo.

- 01 Retrieval of RNA-seq reads from the SRA database
- 02 Conversion of data format and compression 
- 03 Trimming and quality control of reads
- 04 Transcriptome assembly by Trinity 
- 05 Expression quantification by salmon

## Requirements

- Miniconda is required to install `sra-tools`, `trim-galore` and `pigz`.
- Docker is also required to do the analyses in Trinity (04) and salmon (05). 
- Pitagora Workflows in Common Workflow Language (CWL) at https://github.com/pitagora-network/pitagora-cwl is required to run salmon script (05).
