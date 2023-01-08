#!/bin/bash

#author: Avishek Dutta, avdutta@ucsd.edu
#usage: ./taxfin.sh sample_name taxa_name

sample=$1
taxa=$2

#preparing emapper output file for taxfin

tail -n +5 $sample.emapper.annotations > $sample.mod1.annotations

head -n -3 $sample.mod1.annotations > $sample.final.annotations

#extracting particular taxa annotation

./taxfin.py -t $2 -s $1

#removing intermediate files

rm -rf $sample.mod1.annotations

rm -rf $sample.final.annotations
