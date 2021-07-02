# IMAGINE - ***I***n silico ***M***et***AG***enomics Pipel***INE*** (BETA)

**IMAGINE** is a metagenomic workflow which includes filtering, assembling, and binning

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
git clone https://github.com/avishekdutta14/IMAGINE.git
chmod a+x imagine.sh
```
### Installation and validation of dependencies

Most of the tools have their own set of installation protocols and dependencies. They can be obtained from the links mentioned above. This pipeline requires an output of each tool to be piped into the next tool (except for QUAST and the CheckM- since this is the last tool).

## For running IMAGINE
```
./imagine.sh -r sample-R1.fastq.gz -R sample-R2.fastq.gz -s sample_name |& tee -a imagine.txt
```
*sample_name is the name used for all the intermediate files and also serves as a prefix for the final bin names*

### For help

```
./imagine.sh -h
```

## Important consideration

All the parameters set in the shell script are optimized for specific marine system metagenomes. These parameters should be tested and tried while working with metagenomes from other systems/environments. Some thoughts about selecting certain parameters are shared in the following section [How it works?](https://github.com/avishekdutta14/IMagINE/blob/main/README.md#how-it-works) and a detailed description for parameter selection can be obtained from the manuals of each aforesaid tool. Please be cautious about selecting and changing the number of threads selected for each process, as this will vary among systems.

## Important disclosure :warning: :warning: :warning:

Many of the steps/processes/tools use multi-threads for parallelization, and the user can modify it accordingly. This increases resource usage and also decreases the time needed to run processes. This is highly desirable, but it comes with a sacrifice. Many processes used in this pipeline uses probabilistic models. Probabilistic models and many other machine learning models are impacted by the number of threads used since the probabilities and predictions can vary while computing in different threads/CPUs. But, the good news is that these variations are not significant. The results generated will be different (unfortunately), but the difference is small (fortunately). To understand and identify the steps in which you can expect variations are mentioned in the [How it works?](https://github.com/avishekdutta14/IMagINE/blob/main/README.md#how-it-works) section. Morover, the default parameters worked well for specific marine environments and should be modified for other environments. Using default parameters will not gurantee the best result for other environmnets or system (or even other marine systems). To know more on the parameters please consider reading [How it works?](https://github.com/avishekdutta14/IMagINE/blob/main/README.md#how-it-works) section.

## Output files

1. imagine.txt - A log file containing the stdout of the overall workflow. This will help to understand if there is any error in the pipeline. This also gives the track of the versions and syntaxes used for different tools. More importantly, this gives you a sense of the time required for most of the steps (which can be used in the future for time estimations and resource usage). This also contains other information like filtering qualities of reads and also bin qualities.
2. filtered reads: sample_name_filt_R1.fq.gz and sample_name_filt_R2.fq.gz - these are filtered Read 1 and Read 2, respectively.
3. fastp.html and fastp.json - these are the output of fastp, which contains information about read filtering.
4. metaspades_output_sample_name -  output folder containing spades output.
5. quast_output - A folder containing QUAST output from which one can determine the assembly quality, contig sizes, and other information about assemblies. 
6. binning - a folder containing intermediate files (.sam, .bam, and other index files) for mapping and two sub-folders - bins_dir/ and checkm/
7. bins_dir - a sub-folder under binning which contains all the bins
8. checkm - a sub-folder under binning that contains information about the quality of the bins

## How it works?

### Filtering of raw reads

Quality assessment and filtering of raw reads are done using fastp. The user can play around with a lot of [parameters](https://github.com/OpenGene/fastp#all-options) and also modify IMAGINE accordingly. IMAGINE uses default parameters along with -e 30 for removing all the reads whose average quality score is less than 30. This is done to remove low-quality reads since the assembling using metaSPAdes is very sensitive to low-quality data. 

:warning: The -w (number of threads used) is kept to 1 to make the run deterministic (reproducible). The user can change -w to higher values but should be aware of non-reproducible results (the changes in result will be very low and not significant) :zebra:. Since this process does not take a huge time, setting the number of threads to 1 will not increase the run time hugely.

### Assembling and checking assembly qualities

#### Assembly

Assembling will be done using metaSPAdes. This is the most time-taking process. The selection of k-mers can be an important thing, but I wouldn't waste too much time on it. The default k-mer values are set to 21,33,55. Selection of k-mers should be governed by sample type (natural or engineered environment), the complexity of microbiome (high or low diverse :confused: - I know these words are relative), size of the sequenced reads, and other parameters (I might have missed some :worried:). My perspective (might vary among researchers and bioinformaticians), for high complex metagenomes from a natural environment having 150 bp paired-end sequencing, the default parameters (21, 33, 55) should work well; and if you think that the system/environment is defined and are low-complex and the depth of sequencing is very high, you can increase the k-mer (I even went up to 127 with 21, 33, 55, 77, 99, 127 for an engineered environment and got good results :sunglasses:). You can play around with other [parameters](https://cab.spbu.ru/files/release3.15.2/manual.html), and also learn more about spades [here](https://cab.spbu.ru/files/release3.15.2/manual.html).

:warning: The resource usage should be set depending on the resource available and the data size. The maximum threads (-t) and RAM (-m) are set to 20 and 300 GB. The good thing is that the actual amount of RAM consumed will be lower for many steps. There are two main steps done by SPAdes assembler viz. 1. Read correction and 2. Assembly. For assembly, similar number of threads should give reproducible results, but for the Read corrections (done using BayesHammer), I found that even for a similar number of threads, the results might vary. I feel that this variation is governed by resource usage by other processes on the computer/server system that is being used. One can stop the read correction step and only use the assembler to get reproducible results, but using read correction results in high-quality assemblies (developer recommendation). I feel that one should use the read correction step since the results are not very different.

#### Quality assessment of assemblies

The qualities of the assemblies are checked using QUAST. There are different outputs in QUAST that can be used for assembly assessment. N50 values, L50 values, longest contigs, the size distribution of contigs are some of the parameters to look for to understand the assembly quality. One can also use metaQUAST, which has some enhanced features, but for the sake of resource usage and run time, the default is set to QUAST. Details of QUAST can be found [here](http://quast.sourceforge.net/quast.html)

### Binning and checking bin qualities

#### Binning

Binning is done using metabat2, and the mapping/alignment of reads is done using bwa to generate alignment files, which can be further converted to an abundance profile using jgi_summarize_bam_contig_depths (a tool present in the metabat2 [repository](https://bitbucket.org/berkeleylab/metabat/src/master/)). bwa mem ([details here](http://bio-bwa.sourceforge.net/bwa.shtml)) is used for alignment. The user can also use bowtie2 for this. If someone wants to use bowtie2 for the alignments, please contact me. I can modify the script accordingly.

Samtools is used convert .sam file to .bam file and to sort the .bam file since the input of jgi_summarize_bam_contig_depths should be a sorted .bam file. There are also many other piped samtools syntaxes available which can be replaced here. For the clarity of the script and breaking things clearly, conversion of sam to bam and sorting bam file is done in two separate steps.

Then comes metabat2 (finally!!!!), which will help to bin based on abundance and tetranucleotide frequency of the contigs. Though the abundance profile is optional, I would recommend using the abundance profile for better binning. I have changed the minimum size of a contig for binning (-m) from 2500 (default) to 1500 since I  wanted to consider the smaller contigs (but if you want to stick with the default value, you can remove the -m flag). For more details please refer the metabat2 [manual](https://bitbucket.org/berkeleylab/metabat/src/master/). Here comes the good part :grinning:, thanks to the developers :pray: that metabat2 can be reproducible, though it has some sections to pick things (again probabilities/predictabilities). You can set seed values to make it reproducible. I chose a random number 1234 (it came to my mind when writing the script) as a seed for the script. You can modify it if you want.

#### Checking Bin qualities

Last but not least is checking the bin qualities. Bin qualities are checked using the CheckM tool. Bins can be referred to as high-quality draft (>90% completeness, <5% contamination), medium-quality draft (>50% completeness, <10% contamination) or low-quality draft (<50% completeness, <10% contamination) MAGs as suggested by [Bowers et al., 2017](https://www.nature.com/articles/nbt.3893)

## For bin segregation mag_extract.py can be used

mag_extract.py helps in segregating the bins based on quality, as mentioned in Bowers et al., 2017. For running it, place the script in the folder where the bin output folder are present. Rename the bin containing folder to bins_dir (If IMAGINE is used, the folder will be already named as bins_dir/). Also, place the checkm quality (i.e., bin_stats_ext.tsv) information out to the folder in which mag_extract.py is present. The required checkm input can be obtained from the storage folder (checkm_ouptut/storage/bin_stats_ext.tsv) under the checkm output  (i.e., bin_stats_ext.tsv).

This script requires python3,  pandas, and numpy (python libraries).

mag_extract.py can be ran using the following command

```
chmod a+x mag_extract.py
./mag_extract.py
```
mag_extract.py can also be added to PATH, but the script should be implemented in a folder where bins_dir/ and bin_stats_ext.tsv is present

#### The output of mag_extract.py

1. checkm_bin_quality.csv - Information about bins segregated in high-, medium-, and low- quality drafts
2. 3 folders viz. high_qual_draft, medium_qual_draft, and low_qual_draft containing high-, medium-, and low- quality bins as per checkm classification

## For downstream analyses (mainly functional and taxonomic annotations) with IMAGINE and other metagenome workflow outputs (Tips and Tricks) :gift:

### For annotating filtered reads for taxonomic affiliation

[Kaiju](http://kaiju.binf.ku.dk/) can be used for this. For offline use, please visit the Kaiju GitHub [link](https://github.com/bioinformatics-centre/kaiju). Do not forget to download the [reference database](http://kaiju.binf.ku.dk/server) for Kaiju if you are using the offline version. In this step, you will get an idea of the taxonomic distribution of different domains of life (depending on the database you are using you can also get a rough idea of the eukaryotic population distribution).

### For annotating assembled contigs (whole metagenome)

1. [Kaiju](http://kaiju.binf.ku.dk/)- The same thing as before. Here, the classification may be resolved a bit better due to read assembly. But be aware, the distribution here is not directly proportional to the abundance of taxa in this step.
2. [Prodigal](https://github.com/hyattpd/Prodigal) followed by annotation using [KEGG](https://www.genome.jp/kegg/)  or other databases - Prodigal is a fantastic tool in deciphering protein-coding genes for prokaryotic genomes. Be sure to select the [metagenome mode](https://github.com/hyattpd/Prodigal) for this step. Once you obtain the protein/amino acid sequences from prodigal, you can use [GhostKOALA server](https://www.kegg.jp/ghostkoala/), a KEGG-based annotation server. 
3. [Prokka](https://github.com/tseemann/prokka) (a fast one) - I really like Prokka because it will give you a sense of the metagenomic inventory (rapidly). Prokka also uses prodigal. So if you are using Prokka, you will also get the translated amino sequences from here :tada:. This is an offline tool. Be sure to select the metagenome mode. 
4. [IMG Annotation Pipeline](https://img.jgi.doe.gov/docs/pipelineV5/) - IMG annotation pipeline can also be used. It will give you both holistic and detailed view of the metagenome inventory. There are also many other downstream analysis tools present in the [online portal](https://img.jgi.doe.gov/cgi-bin/mer/main.cgi). This is an online tool. Please review the submission/privacy policy before submitting the data.
5. [eggNOG](http://eggnog5.embl.de/#/app/home) - It has got both online and [offline](https://github.com/eggnogdb/eggnog-mapper) versions. The [online version](http://eggnog-mapper.embl.de/) has some restrictions on the amount of data that can be uploaded. You can find the overall workflow for eggNOG [here](http://eggnog-mapper.embl.de/static/emapper_workflow.png).
6. [MG-RAST](https://www.mg-rast.org/) - MG-RAST has both online and offline versions. Please review the submission/privacy policy before submitting the data.

### For annotating MAGs/Genomes

1. [GTDB-Tk](https://ecogenomics.github.io/GTDBTk/) (for taxonomic affiliation) - This tool uses [Genome Taxonomy Database](https://gtdb.ecogenomic.org/) for taxonomic annotation of MAGs or Genomes
2. [Prokka](https://github.com/tseemann/prokka) (a fast one) - Same as mentioned [before](https://github.com/avishekdutta14/IMAGINE#for-annotating-assembled-contigs-whole-metagenome). But be sure to select the correct mode of annotation. And use the correct flag for [-kingdom](https://github.com/tseemann/prokka#command-line-options). You can also play around with the other [parameters](https://github.com/tseemann/prokka#command-line-options)
3. [Prodigal](https://github.com/hyattpd/Prodigal) followed by annotation using KEGG or other databases - Same as mentioned [before](https://github.com/avishekdutta14/IMAGINE#for-annotating-assembled-contigs-whole-metagenome). But be sure to use the correct parameters. For genomes use [BLASTKoala](https://www.kegg.jp/blastkoala/) server for KEGG-based annotation.
4. [RAST](https://rast.nmpdr.org/rast.cgi) - RAST annotation is done based on subsystems technology. It is an online platform and gives you a wide array of results.
5. [PGAP](https://www.ncbi.nlm.nih.gov/genome/annotation_prok/) - This tool can be found both [online](https://www.ncbi.nlm.nih.gov/genome/annotation_prok/) and [offline](https://github.com/ncbi/pgap). The offline tool is appropriate for researchers planning on submitting genomes to NCBI. The online version can be accessed after submission of the genome to NCBI database. An overview of the pipeline can be found [here](https://www.ncbi.nlm.nih.gov/genome/annotation_prok/process/).
6. [eggNOG](http://eggnog5.embl.de/#/app/home) - This tool can also be used for genome. Please refer to [metagenome annotation section](https://github.com/avishekdutta14/IMAGINE/blob/main/README.md#for-annotating-assembled-contigs-whole-metagenome) for more details.

## How to cite (IMAGINE)

1. fastp - Shifu Chen, Yanqing Zhou, Yaru Chen, Jia Gu, fastp: an ultra-fast all-in-one FASTQ preprocessor, Bioinformatics, Volume 34, Issue 17, 01 September 2018, Pages i884–i890, https://doi.org/10.1093/bioinformatics/bty560
2. MetaSPAdes - Nurk S, Meleshko D, Korobeynikov A, Pevzner PA. metaSPAdes: a new versatile metagenomic assembler. Genome Res. 2017;27(5):824-834. doi:10.1101/gr.213959.116
3. QUAST- Alexey Gurevich, Vladislav Saveliev, Nikolay Vyahhi, Glenn Tesler, QUAST: quality assessment tool for genome assemblies, Bioinformatics, Volume 29, Issue 8, 15 April 2013, Pages 1072–1075, https://doi.org/10.1093/bioinformatics/btt086
4. bwa- Heng Li, Richard Durbin, Fast and accurate short read alignment with Burrows–Wheeler transform, Bioinformatics, Volume 25, Issue 14, 15 July 2009, Pages 1754–1760, https://doi.org/10.1093/bioinformatics/btp324
5. samtools- Li H, Handsaker B, Wysoker A, et al. The Sequence Alignment/Map format and SAMtools. Bioinformatics. 2009;25(16):2078-2079. doi:10.1093/bioinformatics/btp352
6. metabat2- Kang DD, Li F, Kirton E, et al. MetaBAT 2: an adaptive binning algorithm for robust and efficient genome reconstruction from metagenome assemblies. PeerJ. 2019;7:e7359. Published 2019 Jul 26. doi:10.7717/peerj.7359
7. checkM- Parks DH, Imelfort M, Skennerton CT, Hugenholtz P, Tyson GW. CheckM: assessing the quality of microbial genomes recovered from isolates, single cells, and metagenomes. Genome Res. 2015;25(7):1043-1055. doi:10.1101/gr.186072.114

If you are using any other downstream annotation tools mentioned in this documentation, please cite them in the literature.

## Disclaimer

This tool and the suggested workflow is strictly intended for educational and academic purpose. The results for different tools might vary depending on the input dataset.
