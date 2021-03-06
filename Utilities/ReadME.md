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

This script is based on the methods reported in [Herv?? et al., 2020](10.7717/peerj.8614) and [Hua et al., 2019](10.1038/s41467-019-12574-y).
