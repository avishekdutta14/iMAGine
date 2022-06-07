#!/bin/bash

if [ $(which fastp 2>/dev/null) ]; then
  echo "fastp found"
else
  echo "fastp not found"
fi

if [ $(which metaspades.py 2>/dev/null) ]; then
  echo "metaspades.py found"
else
  echo "metaspades.py not found"
fi

if [ $(which quast.py 2>/dev/null) ]; then
  echo "quast.py found"
else
  echo "quast.py not found"
fi

if [ $(which bwa 2>/dev/null) ]; then
  echo "bwa found"
else
  echo "bwa not found"
fi

if [ $(which samtools 2>/dev/null) ]; then
  echo "samtools found"
else
  echo "samtools not found"
fi

if [ $(which jgi_summarize_bam_contig_depths 2>/dev/null) ]; then
  echo "jgi_summarize_bam_contig_depths found"
else
  echo "jgi_summarize_bam_contig_depths not found"
fi

if [ $(which metabat2 2>/dev/null) ]; then
  echo "metabat2 found"
else
  echo "metabat2 not found"
fi

if [ $(which checkm 2>/dev/null) ]; then
  echo "checkm found"
else
  echo "checkm not found"
fi
