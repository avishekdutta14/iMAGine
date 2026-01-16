#!/bin/bash

# author: Avishek Dutta, avishek.dutta@uga.edu

helpFunction()
{
   echo -e "\t Usage: ./imagine.sh -r LMG2001_200121_7-R1.fastq.gz -R LMG2001_200121_7-R2.fastq.gz -s sample_name |& tee -a imagine.txt"
   echo -e "\t-r read 1"
   echo -e "\t-R read 2"
   echo -e "\t-s name of the sample (modifier) given to intermediated files"
   echo -e "\t-h help"
   exit 1 # Exit script after printing help
}

while getopts r:R:s:h opt
do
   case "${opt}" in
      r ) read1=${OPTARG};;
      R ) read2=${OPTARG};;
      s ) name=${OPTARG};;
      h ) helpFunction ;;
   esac
done


START=$(date +%s)

## filtering step

## ml fastp/0.23.2-GCC-11.3.0

fastp -i ${read1} -I ${read2} -o ${name}_filt_R1.fq.gz -O ${name}_filt_R2.fq.gz -e 30 -w 1 -j fastp_${name}.json -h fastp_${name}.html &&

## assembling step

## ml fastp/0.23.2-GCC-11.3.0

spades.py -1 ${name}_filt_R1.fq.gz -2 ${name}_filt_R2.fq.gz -k 21,33,55 -o spades_output_${name} --isolate &&

## checking quality of the assembly

## ml QUAST/5.2.0-foss-2022a

quast.py spades_output_${name}/contigs.fasta -o quast_output_${name} &&

mkdir genome_dir_${name}

cp spades_output_${name}/contigs.fasta genome_dir_${name}

## checking completeness of the genome

## ml CheckM/1.2.2-foss-2022a

checkm lineage_wf genome_dir_${name} checkm/ -x .fasta -t 1

## assigning taxonomy to the genome

## ml GTDB-Tk/2.3.2-foss-2022a

gtdbtk classify_wf --genome_dir genome_dir_${name}/ --out_dir gtdb_output --skip_ani_screen -x .fasta

## Gene calling

## ml prodigal/2.6.3-GCCcore-11.3.0

prodigal -i genome_dir_${name}/contigs.fasta -o ${name}.genes -a ${name}.proteins.faa

END=$(date +%s)
DIFF=$(( $END - $START ))

echo "It took $DIFF seconds"
