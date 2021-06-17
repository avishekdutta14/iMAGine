# IMAGINE - In silico Metagenomics Pipeline (BETA)

IMAGINE is a metagenomic workflow which includes filtering, assembling, and binning

This workflow includes the following tools which are needed to be installed in the system.

1. [fastp](https://github.com/OpenGene/fastp)
2. [spades assembler](https://github.com/ablab/spades)
3. [QUAST](https://github.com/ablab/quast)
4. [bwa](https://github.com/lh3/bwa)
5. [samtools](https://github.com/samtools/samtools)
6. [metabat2](https://bitbucket.org/berkeleylab/metabat/src/master/)
7. [CheckM](https://github.com/Ecogenomics/CheckM)

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

## Important consideration

All the parameters set in the shell script are optimized for specific marine system metagenome. These parameters should be tested and tried while working with metagenomes from other systems/environments. Some thoughts about selecting certain parameters are shared in the following section [How it works?](https://github.com/avishekdutta14/IMagINE/blob/main/README.md#how-it-works) and detailed description for parameter selection can be obtained from the manuals of each aforesaid tool. Please be cautious about selecting and changing the number of threads selected for each process as this will vary amond systems.

## Important disclosure :warning: :warning: :warning:

Many of the steps/processes/tools uses multi-threads for parallelization and the user can modify it accordingly. This increases the resource usage and also decreases the time needed to run a processes. This is highly desirable, but it comes with a sacrifice. Many processes used in this pipeline usese probabilistic models. Probabilistic models and many other machine learning models are impacted by number of threads used, since the probabilities and predictions can vary while computing in different threads/cpus. But, the good news is that this variations are not significant. The results generated will be different (unfortunately), but the difference is small (fortunately). To understand and identify the steps in which you can expect variations are mentioned in the [How it works?](https://github.com/avishekdutta14/IMagINE/blob/main/README.md#how-it-works) section.  

## Output files

1. imagine.txt - A log file containing the stdout of the overall workflow. This will help to understand if there is any error in the pipeline. This also gives the track of the versions and syntaxes used for different tools. More importantly, this gives you a sense of time required for most of the steps (which can be used in future for time estimations and resource usage). This also contains other information like filtering qulatiies of reads and also bin qualities.
2. filtered reads: sample_name_filt_R1.fq.gz and sample_name_filt_R2.fq.gz - these are filtered Read 1 and Read 2 respectively.
3. fastp.html and fastp.json - these are the output of fastp which contains information about read filtering.
4. metaspades_output_sample_name -  output folder containing spades output.
5. quast_output - A folder contianing QUAST output from which one can determine the assembly quality, contig sizes, and other informations about assemblies. 
6. binning - a folder containg intermediate files (.sam, .bam and other index file) for mapping and two sub-folders - bins_dir/ and checkm/
7. bins_dir - a sub-folder under binning which contains all the bins
8. checkm - contains information about the quality of the bins

## How it works?

### Filtering of raw reads

Quality assessment and filtering of raw reads are done using fastp. The user can play around with a lot of [parameters](https://github.com/OpenGene/fastp#all-options) and also modify IMAGINE accordingly. IMAGINE uses default parameters along with -e 30 for removing all the reads whoes average quality score is less than 30. This is done to remove low quality reads since the assembling using metapsades is very sensetive to low quality data. 

:warning: The -w (number of threads used) is kept to 1 to make the run deterministic (reproducible). The user can change -w to higher values, but should be aware of non-reporducible results (the changes in result will be very low and not significant) :zebra:. Since this process does not take a huge time, setting number of threads to 1 will not increase the run time hugely.

### Assembling and checking assembly qualities

#### Assembly

Assembling will be done using metaSPAdes. This is the most time-taking process. Selection of k-mers can be an important thing, but I wouldn't waste too much time in it. The default k-mer values are set to 21,33,55. Selection of k-mers should be governed by sample type (natural or engineered environment), complexity of microbiome (high or low diverse :confused: - I know these words are relative), size of the sequenced reads, and other parameters (I might have missed some :worried:). My perspective (might vary among researchers and bioinformaticians), for high complex metagenomes from natura environment having 150 bp paired-end sequencing, the default parameters (21, 33, 55) should work well; and if you think that the system/environment is defined and are low complex and the depth of sequencing is very high, you can increase the k-mer (I even went up to 127 with 21, 33, 55, 77, 99, 127 for an engineered environment and got good results :sunglasses:. You can play around with other [parameters](https://cab.spbu.ru/files/release3.15.2/manual.html), and also learn more about spades [here](https://cab.spbu.ru/files/release3.15.2/manual.html).

:warning: The resource usage should be set depending on the resource available and the data size. The maximum threads (-t) and RAM (-m) are set to 20 and 300 GB. Good thing is that the actual amount of RAM consumed will be lower for many steps. There are two main steps done by SPAdes assembler viz. 1. Read correction and 2. Assembly. For assembly, similar number of threads should give reporducible results, but for the Read corrections (done using BayesHammer), I found that even for similar number of threads, the results might vary. I feel that this variations are governed by resources usage by other processes on the computer/server system that is being used. One can stop the read correction step and only use the assembler to get reprocucible results, but using read correction results in high-quality assemblies (developer recommendation). I feel that one should use the read correction step since the results are not very different.

#### Quality assessment of assemblies

Quality of the assemblies are checked using QUAST. There are different outputs in quast which can be used for assembly assessment. N50 values, L50 values, longest contigs, size distribution of contigs are some the parameters to look for to understand the assembly quality. One can also use metaquast which has some enhanced features, but for the sake of resource usage and run time, the default is set to quast. Details of QUAST can be found [here](http://quast.sourceforge.net/quast.html)

### Binning and checking bin qualities

#### Binning

Binning is done using metabat2, and the mapping/alignement of reads are done using bwa to generate alignment files, which can be further converted to an abundance profile using jgi_summarize_bam_contig_depths (a tool present in the metabat2 [repository](https://bitbucket.org/berkeleylab/metabat/src/master/)). bwa mem ([details here](http://bio-bwa.sourceforge.net/bwa.shtml)) is used for alignment. The user can also use bowtie2 for this. If someone wants to use bowtie2 for the alignments, please contact me. I can modify the script accordingly.

Samtools is used convert .sam file to .bam file and to sort the .bam file since the input of jgi_summarize_bam_contig_depths should be a sorted .bam file.

Then comes metabat2 (finally!!!!), which will help to bin based on abundance and tetra nucleotide frequency of the contigs. Though the abundance profile is optional, but I would recommend to use the abundance profile for better binning. I have changed minimum size of a contig for binning (-m) from 2500 (default) to 1500, since I  wanted to consider the smaller contigs (but if you want to stick with the default value, you can remove the -m flag). For more details please refer the metabat2 [manual](https://bitbucket.org/berkeleylab/metabat/src/master/). Here comes the good part :grinning:, thanks to the developers :pray: that metabat2 can be reproducible, though it have some sections to pick things (again probabilities/predictibilities). You can set seed values to make it reproducible. I chose a random number 1234 (it came to my mind when writing the script) as seed for the script. You can modify it if you want. 

#### Checking Bin qualities

Last but not the least, is checking the bin qualities. Bin qualities are checked using CheckM tool. Bins can be referred to as high-quality draft (>90% completeness, <5% contamination), medium-quality draft (>50% completeness, <10% contamination) or low-quality draft (<50% completeness, <10% contamination) MAGs as suggested by [Bowers et al., 2017](https://www.nature.com/articles/nbt.3893)

## How to cite
