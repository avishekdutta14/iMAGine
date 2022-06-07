# This folder is for associated scripts for iMAGine

binviz.py is used for vizulizing Contamination vs Completeness plots. The coverage informations is calculated from the headers of the contigs here. To get accurate coverage values, I would suggest to generated from the alingned files under binning folder. This script will require matplotlib python library. The input of this script is the bins_dir and bin_stats_ext.tsv (present insider checkm/storage/ folder). The output will be in scatter_plot_binviz.pdf and refined_stats.csv.
