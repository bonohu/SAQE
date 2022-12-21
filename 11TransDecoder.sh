#!/bin/sh
# TransDecoder: predict protein coding regions from transcripts

# filename for Trinity output (default: Trinity.fasta)
transcript=Trinity.fasta

# Run transdecoder 
TransDecoder.LongOrfs -t $transcript
TransDecoder.Predict -t $transcript
