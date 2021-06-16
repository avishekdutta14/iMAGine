# IMAGINE - In silico Metagenomic Pipeline (BETA)

This is a metagenomic workflow which starts from filtering the raw reads and ends in binning metagenome-assembled genomes.

This workflow includes the following tools which are needed to be installed in the system.

1. [fastp](https://github.com/OpenGene/fastp)
2. [spades assembler](https://github.com/ablab/spades)
3. [QUAST](https://github.com/ablab/quast)
4. [bwa](https://github.com/lh3/bwa)
5. [metabat2](https://bitbucket.org/berkeleylab/metabat/src/master/)
6. [CheckM](https://github.com/Ecogenomics/CheckM)

## Downloading 
```
git clone repository
chmod a+x imagine.sh
```
### Installation and validation of dependencies

Most of the tools has its own set of installation protocol and dependencies. They can be obtained from the links mentioned above. This pipeline requires output of each individual tool to be piped into the next tool (except for QUAST and obiously the CheckM- since this is the last tool).

## For running IMAGINE
```
./imagine.sh -r sample-R1.fastq.gz -R sample-R2.fastq.gz -s sample_name |& tee -a imagine.txt
```
### For help

```
./imagine.sh -h
```

## Important consideration:

All the parameters set in the shell script are optimized for specific marine system metagenome. These parameters should be tested and tried while working with metagenomes from other systems/environments. Some thoughts about selecting certain parameters are shared in the following section [How it works?](https://github.com/avishekdutta14/IMagINE/blob/main/README.md#how-it-works) and detailed description for parameter selection can be obtained from the manuals of each aforesaid tool.

## Output files

1. imagine.txt - A log file containing the stdout of the overall workflow. This will help to understand if there is any error in the pipeline. This also gives the track of the versions and syntaxes used for different tools. More importantly, this gives you a sense of time required for most of the steps (which can be used in future for time estimations and resource usage). This also contains other information like filtering qulatiies of reads and also bin qualities.
2. fastp.html and fastp.json - these are the output of fastp which contains information about read filtering.
3. metaspades_output_sample_name -  output folder containing spades output.
4. quast_output - A folder contianing QUAST output from which one can determine the assembly quality, contig sizes, and other informations about assemblies. 
5. binning - a folder containg intermediate files (.sam, .bam and other index file) for mapping and two sub-folders - bins_dir/ and checkm/
6. bins_dir - a sub-folder under binning which contains all the bins
7. checkm - contains information about the quality of the bins

## How it works?

### Filtering of raw reads

Quality assessment and filtering of raw reads are done using fastp. 

### Assembling and checking assembly qualities

### Binning and checking bin qualities

## How to cite
