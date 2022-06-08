#!/usr/bin/env python3

import pandas as pd
import argparse
import os
import subprocess
from datetime import datetime

"""
This script should be placed inside the folder having all the bins

Usage: mag_abund_final.py -s ../depth1_map.sam -n depth1 -b bins_dir
'-s', '--sam_file' -> name of the sam files used for making the bins or a sam file where all the reads are mapped to a contig_fate
'-n', '--sample_name' -> name of the sample for incorporating in the output
'-b', '--bin_folder' -> name of the folder in which bins are present
"""

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--sam_file', help = 'Name of SAM file')
parser.add_argument('-n', '--sample_name', help = 'Sample Name')
parser.add_argument('-b', '--bin_folder', help = 'Bin Folder')


args = parser.parse_args()

sam_filename = '{}'.format(args.sam_file)
sample_name = '{}'.format(args.sample_name)
bin_folder_name = '{}'.format(args.bin_folder)


# module for assessing contig fate in each bin
#path = '.'
files_in_dir = [f for f in os.listdir(bin_folder_name) if f.endswith('.fa')]
print("There are {} number of bins in the bin directory.".format(len(files_in_dir)))
for f in files_in_dir:
    string=","+f
    string=string.replace(".fa","")
    with open(os.path.join(bin_folder_name, f),'r') as f1:
        targets = [line for line in f1 if ">" in line] # picking lines having ">"
        targets = [w.replace('>', '') for w in targets] # replacing ">" with blank
        new_lines = [''.join([x.strip(), string, '\n']) for x in targets] # adding a string at the end of each line
    f1.close()
    with open('contig_fate_{}.txt'.format(f), 'w') as f2:
        f2.writelines(new_lines)
    f2.close()
os.system("cat *.fa.txt > contig_fate.txt")
os.system("rm -rf *.fa.txt")

now = datetime.now()
dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
print("Contigs fate was generated at:", dt_string)

# running subprocesses for samtools and pileup.sh

input_sam=sam_filename
output_sam=sample_name+"_F904.sam"

# for samtools -F 904 is used for removing unmapped reads and removing any secondary or supplementary alignment

with open(output_sam,'w') as f5:
    p1 = subprocess.run(["samtools", "view", "-h", "-F", "0x904", input_sam], stdout=f5, universal_newlines=True)

now = datetime.now()
dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
print("Filtering based on -F 904 was completed at:", dt_string)

# Calculates per-scaffold or per-base coverage information from an unsorted sam or bam file.
# 32bit=t flag was given for overcoming the following error
# Note: Coverage capped at 65535; please use the flag 32bit for higher values.

subprocess.run(["pileup.sh", "in={}".format(output_sam), "out=pileup_result.txt", "32bit=t"])

now = datetime.now()
dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
print("Summary of filtered map reads were generated at:", dt_string)

# reading contig fate data

bin_fate = pd.read_csv("contig_fate.txt", names=('#ID', 'bin_name'))

# reading mapped data (output of pileup.sh)

mapped_reads = pd.read_csv("pileup_result.txt", sep='\t')

# merging two datasets

merged_df = bin_fate.merge(mapped_reads, how='left', on='#ID')

# selecting columns from merged_df

merged_df_selected = merged_df[['#ID', 'bin_name', 'Plus_reads', 'Minus_reads']]

# grouping based on bin_name

group_df = merged_df_selected.groupby('bin_name').sum()

# summing plus reads and minus reads

sum_column = group_df["Plus_reads"] + group_df["Minus_reads"]

# saving the total read sum into a new columns

group_df["total_mapped_reads"] = sum_column

# saving the final result

group_df.to_csv('mapped_reads_per_bin_{}.csv'.format(sample_name))

now = datetime.now()
dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
print("The run was completed at:", dt_string)
print("The result is present in mapped_reads_per_bin_{}.csv".format(sample_name))
