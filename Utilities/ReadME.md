# This folder is for associated scripts for iMAGine

## binviz.py

@requires: python3, Pandas, matplotlib, biopython

binviz.py is used for vizualizing contamination vs completeness plots. This plots bins having contamination lower than 20 %. The coverage informations is calculated from the headers of the contigs here. To get accurate coverage values, I would suggest to generate coverage from the alingned files under binning folder. One can also use the mag_abund.py tool to get a better overview of the number of reads mapped to particular bins. This script will require matplotlib python library. 

_Inputs_

1. bins_dir (output of iMAGine where alls the bins are present) and 
2. bin_stats_ext.tsv (present insider checkm/storage/ folder). 

_Outputs_

1. refined_stats.csv
2. scatter_plot_binviz.pdf

To run binviz.py, copy the script to the location where bins_dir (output of iMAGine where alls the bins are present) and bin_stats_ext.tsv (present insider checkm/storage/ folder) are present and then use the following command

```
chmod a+x binviz.py
./binviz.py
```
One can also declare the script to the $PATH.

## mag_abund.py

@requires: python3, Pandas, samtools, BBMap (pileup.sh script)

mag_abund.py is a tool which gives information about number of reads mapped to particular bin.

To run mag_abund.py

```
./mag_abund.py -s name_of_samfile.sam -n sample_name_for_output_mod -b name_of_the_bin_folder
```
_Inputs_

1. samfile - name of the sam files used for making the bins or a sam file where all the reads are mapped to a contig_fate
2. sample_name - name of the sample for incorporating in the output
3. bin_folder - name of the folder in which bins are present

_Outputs_

The main output of this script is **mapped_reads_per_bin_test_output_sample_name.csv**. 

Other output are 
1. sample_name_F904.sam (filtered sam file base on F904 - where unmapped reads and reads mapped to more than one location were removed by using samtools) 
2. contig_fate.txt (distribution of contigs in different bins), and 
3. pileup_result.txt (result from pileup.sh script- lot of mapping information in it if the user is interested in).

How it works? -> it looks at the contigs binned into each bin, removes unmapped reads and reads mapped to more than one location, extracts mapping information for each contigs from filtered sam file and combines results to get the final outcome.

This script is based on the methods reported in [Hervé et al., 2020](10.7717/peerj.8614) and [Hua et al., 2019](10.1038/s41467-019-12574-y).

## gene_fold_counter.sh

@requires: python3, Pandas, samtools, BBMap (pileup.sh script), gene_fold_counter.py, and emapper annotation output

gene_fold_counter.sh is a tool which counts the number of a particular gene (based on KEGG orthology result in emmapper annotation output) and calculate the coverage of those gene by mapping the genes back to the contigs, calculating the average coverage of the contigs, and mapping back average contig coverage to the gene.

To run gene_fold_counter.sh

Make sure gene_fold_counter.py is in the same folder in which gene_fold_counter.sh is present. gene_fold_counter.sh can also be declared to the $PATH.

```
./gene_fold_counter.sh name_of_the_sample sam_file annotation_file
```

_Inputs_

1. name_of_the_sample - this is used to modify the output
2. sam_file - location and name of the sam_file (output of iMAGine - present inside binning directory)
3. annotation_file - name of the annotation file (the output of emapper.py)

_Outputs_

The main output is **gene_fold_counter_result_sample_name.csv**

1. sample_name_F904.sam (filtered sam file base on F904 - where unmapped reads and reads mapped to more than one location were removed by using samtools).
2. pileup_result_sample_name.txt (result from pileup.sh script- lot of mapping information in it if the user is interested in).
3. sample_name.final.annotations (trimmed annotation files after first 4 and last 3 lines; the are first 4 and last 3 lines contains time-stamp, metadata, and syntax from emapper)

How it works? -> gene_fold_counter.sh is a tool which counts the number of a particular gene (based on KEGG orthology result in emmapper annotation output) and calculate the coverage of those gene by mapping the genes back to the contigs, calculating the average coverage of the contigs, and mapping back average contig coverage to the gene. It removes unmapped reads and reads mapped to more than one location from the .sam file and uses pileup.sh script to calculate the average coverage of each contigs.

## taxfin.sh
@requires: python3, pandas

taxfin.sh is a tool which is used for filtering functional annotations based on taxa from emapper output

To run taxfin.sh

Make sure taxfin.py is in the same folder in which taxfin.sh is present. taxfin.sh can also be declared to the $PATH. The emapper output (sample_name.emapper.annotations) should be present in the current folder.

```
./taxfin.sh sample_name taxa_name
```

_Inputs_

1. sample_name - the sample name used for emapper annotation (for e.g.: sample_name.emapper.annotations)
2. emapper output - sample_name.emapper.annotations (automatically detected by the script)
3. taxa_name - the taxa which the user want to keep in the output (anyone of the following input: Virus/Bacteria/Archaea)

_Outputs_

1. sample_name.emapper.annotations_taxa_name.csv - annotations related to particular taxa
2. sample_name.emapper_taxa_name_counts.csv - counts of different other taxa at lower taxonomic level
