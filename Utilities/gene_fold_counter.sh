#!/bin/bash

sample_name=$1
sam_file=${2}
annotation=${3}

START=$(date +%s)

samtools view -h -F 0x904 ${sam_file} > ${sample_name}_F904.sam

pileup.sh in=${sample_name}_F904.sam out=pileup_result_${sample_name}.txt

tail -n +5 $annotation > $sample_name.mod1.annotations

head -n -3 $sample_name.mod1.annotations > $sample_name.final.annotations

./gene_fold_counter.py -n $sample_name -a $sample_name.final.annotations

rm -rf $sample_name.mod1.annotations

END=$(date +%s)
DIFF=$(( $END - $START ))

echo "It took $DIFF seconds"