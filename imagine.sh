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

fastp -i ${read1} -I ${read2} -o ${name}_filt_R1.fq.gz -O ${name}_filt_R2.fq.gz -e 30 -w 1 -j fastp_${name}.json -h fastp_${name}.html &&

## assembling step

metaspades.py -1 ${name}_filt_R1.fq.gz -2 ${name}_filt_R2.fq.gz -k 21,33,55 -o metaspades_output_${name} -t 20 -m 300 &&

quast.py metaspades_output_${name}/contigs.fasta -o quast_output_${name} &&

## binning step

mkdir binning_${name} &&

cp metaspades_output_${name}/contigs.fasta binning_${name} &&

cd binning_${name} &&

bwa index contigs.fasta &&

bwa mem -t 20 contigs.fasta ../${name}_filt_R1.fq.gz ../${name}_filt_R2.fq.gz > ${name}_map.sam &&

samtools view -S -b ${name}_map.sam > ${name}_map.bam &&

samtools sort -o ${name}_map_sorted.bam -O bam ${name}_map.bam &&

jgi_summarize_bam_contig_depths --outputDepth ${name}_depth.txt ${name}_map_sorted.bam &&

metabat2 -i contigs.fasta -a ${name}_depth.txt -o bins_dir/${name}_bin --seed 1234 -m 1500 -v &&

## checking bin quality

checkm lineage_wf bins_dir/ checkm/ -x .fa -t 25 &&

END=$(date +%s)
DIFF=$(( $END - $START ))

echo "It took $DIFF seconds"
