#!/bin/sh
# TransDecoder: predict protein coding regions from transcripts

transcript=Trinity.fasta

TransDecoder.LogOrfs $transcript
TransDecoder.Predict $transcript
