# IMAGINE - In silico MetAGenomic PipelINE (BETA)

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
## Important consideration:

All the parameters set in the shell script are optimized for specific marine system metagenome. These parameters should be tested and tried while working with metagenomes from other systems/environments
